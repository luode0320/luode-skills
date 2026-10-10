#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全平台视频内容提取脚本 (字幕提取 / 标清视频 / 音频下载)
- 缓存复用机制: 相同视频直接命中本地缓存，无需重复下载
- LRU 轮转清理: 严格保留最近 3 个历史任务，自动清理旧临时文件，防磁盘膨胀
- B 站专属通道: 零外部依赖，极速提取官方/AI字幕与 360P 标清流
- 通用全网通道: 调度 yt-dlp 支持全网主流视频提取
"""

import sys
import os
import re
import glob
import json
import argparse
import subprocess
import urllib.request
import urllib.parse
from datetime import timedelta

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 默认全局缓存目录 (跨会话统一，不散落脏数据)
DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".qoder", "cache", "video-summary")
MAX_HISTORY_COUNT = 3

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com'
}

def format_seconds(seconds: float) -> str:
    td = timedelta(seconds=int(seconds))
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

# ======================= 缓存管理与历史轮转 =======================

def rotate_cache_history(cache_dir: str, max_history: int = MAX_HISTORY_COUNT):
    """
    自动清理旧临时数据，严格保留最近 max_history (3) 个历史视频/字幕任务。
    以主文件 (mp4/mkv/webm/subtitle.txt/srt) 的 mtime 排序判定。
    """
    if not os.path.exists(cache_dir):
        return

    # 收集缓存目录中所有主要产物文件
    valid_exts = ('.mp4', '.mkv', '.webm', '.flv', '.subtitle.txt', '.srt', '.vtt')
    files = [
        os.path.join(cache_dir, f) for f in os.listdir(cache_dir)
        if os.path.isfile(os.path.join(cache_dir, f)) and f.lower().endswith(valid_exts)
    ]

    # 按所属基础文件名分组（一个任务可能包含 .mp4 + .txt + .json）
    # 提取前缀作为任务分组标识 (去掉 .360p.mp4, .subtitle.txt 等后缀)
    groups = {}
    for f in files:
        base = os.path.basename(f)
        group_key = re.sub(r'(\.360p|\.subtitle|\.low|_low)?\.(mp4|mkv|webm|flv|txt|srt|vtt)$', '', base, flags=re.I)
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(f)

    if len(groups) <= max_history:
        return

    # 按该组最新文件的修改时间排序 (从新到旧)
    sorted_groups = sorted(
        groups.items(),
        key=lambda item: max(os.path.getmtime(p) for p in item[1]),
        reverse=True
    )

    # 保留前 max_history 个，其余删除
    to_delete_groups = sorted_groups[max_history:]
    for g_key, g_files in to_delete_groups:
        sys.stderr.write(f"[清理] 缓存超过 {max_history} 个历史，自动清理过期任务: {g_key}\n")
        for f in g_files:
            try:
                os.remove(f)
            except Exception as e:
                sys.stderr.write(f"[清理告警] 删除文件失败 {f}: {e}\n")

def check_cached_output(cache_dir: str, prefix_key: str, prefer_subtitle: bool = True) -> tuple[str | None, str | None]:
    """
    检查是否已有缓存：
    返回 (output_file, extracted_type) 或 (None, None)
    """
    if not os.path.exists(cache_dir):
        return None, None

    # 先查字幕
    if prefer_subtitle:
        sub_matches = glob.glob(os.path.join(cache_dir, f"*{prefix_key}*subtitle*.txt")) + \
                      glob.glob(os.path.join(cache_dir, f"*{prefix_key}*.srt"))
        if sub_matches:
            target = max(sub_matches, key=os.path.getmtime)
            if os.path.getsize(target) > 0:
                os.utime(target, None) # 刷新访问时间
                return target, "subtitle"

    # 再查视频
    video_matches = glob.glob(os.path.join(cache_dir, f"*{prefix_key}*360p*.mp4")) + \
                    glob.glob(os.path.join(cache_dir, f"*{prefix_key}*_low*.*")) + \
                    glob.glob(os.path.join(cache_dir, f"*{prefix_key}*.mp4"))
    if video_matches:
        target = max(video_matches, key=os.path.getmtime)
        if os.path.getsize(target) > 0:
            os.utime(target, None) # 刷新访问时间
            return target, "video_low"

    return None, None

# ======================= 工具与通道 =======================

def ensure_yt_dlp() -> bool:
    try:
        import yt_dlp
        return True
    except ImportError:
        pass

    try:
        res = subprocess.run(["yt-dlp", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0:
            return True
    except Exception:
        pass

    sys.stderr.write("[Info] 未检测到 yt-dlp，正在通过 pip 自动安装以支持全网视频...\n")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "-q"])
        return True
    except Exception as e:
        sys.stderr.write(f"[Warn] 自动安装 yt-dlp 失败: {e}\n")
        return False

def resolve_bvid(input_str: str) -> tuple[str, int | None]:
    part_num = None
    p_match = re.search(r'[?&]p=(\d+)', input_str)
    if p_match:
        part_num = int(p_match.group(1))

    if 'b23.tv' in input_str:
        try:
            req = urllib.request.Request(input_str.strip(), headers=DEFAULT_HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                input_str = resp.geturl()
                if not part_num:
                    p_match = re.search(r'[?&]p=(\d+)', input_str)
                    if p_match:
                        part_num = int(p_match.group(1))
        except Exception as e:
            sys.stderr.write(f"[Warn] 解析 B 站短链接失败: {e}\n")

    bv_match = re.search(r'(BV[a-zA-Z0-9]{10})', input_str)
    if not bv_match:
        raise ValueError(f"无法从输入中找到有效 BV 号: {input_str}")
    return bv_match.group(1), part_num

def fetch_json(url: str, headers=None) -> dict:
    req = urllib.request.Request(url, headers=headers or DEFAULT_HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))

def download_bilibili_stream(url: str, output_path: str):
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        total_size = int(resp.headers.get('Content-Length', 0))
        downloaded = 0
        with open(output_path, 'wb') as f:
            while True:
                chunk = resp.read(1024 * 512)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = downloaded / total_size * 100
                    sys.stderr.write(f"\r[下载中] {downloaded/1024/1024:.2f}MB / {total_size/1024/1024:.2f}MB ({percent:.1f}%)")
                    sys.stderr.flush()
        sys.stderr.write("\n")

# ======================= Bilibili 业务处理 =======================

def process_bilibili(input_target: str, target_part: int | None, mode: str, output_dir: str) -> dict:
    bvid, parsed_part = resolve_bvid(input_target)
    final_part = target_part or parsed_part or 1
    cache_key = f"{bvid}_P{final_part}"

    # 1. 优先检查本地是否命中历史缓存
    cached_file, cached_type = check_cached_output(output_dir, cache_key, prefer_subtitle=(mode != 'video-low'))
    if cached_file:
        sys.stderr.write(f"[缓存命中] 发现本地最近历史缓存，跳过重复下载: {os.path.basename(cached_file)}\n")
        rotate_cache_history(output_dir)
        return {
            "status": "success",
            "platform": "bilibili",
            "bvid": bvid,
            "part_index": final_part,
            "cached": True,
            "has_subtitle": (cached_type == "subtitle"),
            "extracted_type": cached_type,
            "output_file": os.path.abspath(cached_file),
            "file_size_mb": round(os.path.getsize(cached_file) / 1024 / 1024, 2)
        }

    # 2. 未命中缓存，获取视频元数据
    view_api = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    view_data = fetch_json(view_api)
    if view_data.get('code') != 0:
        raise RuntimeError(f"获取 B 站视频信息失败: {view_data.get('message')}")

    video_info = view_data['data']
    video_title = video_info.get('title', bvid)
    pages = video_info.get('pages', [])
    if not pages:
        raise RuntimeError("该视频未包含有效的分P数据")

    part_idx = final_part - 1
    if part_idx < 0 or part_idx >= len(pages):
        part_idx = 0
        final_part = 1

    target_page = pages[part_idx]
    cid = target_page['cid']
    part_title = target_page.get('part', f'P{final_part}')
    duration = target_page.get('duration', 0)

    safe_title = re.sub(r'[\\/*?:"<>|]', '_', f"{bvid}_P{final_part}_{part_title}")[:60]
    res = {
        "status": "success",
        "platform": "bilibili",
        "title": video_title,
        "part_index": final_part,
        "total_parts": len(pages),
        "part_title": part_title,
        "duration_formatted": format_seconds(duration),
        "cached": False,
        "has_subtitle": False,
        "extracted_type": None,
        "output_file": None
    }

    # 3. 尝试提取字幕
    if mode in ['auto', 'sub-only']:
        sub_api = f"https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}"
        sub_data = fetch_json(sub_api)
        subtitles = sub_data.get('data', {}).get('subtitle', {}).get('subtitles', [])
        if subtitles:
            chosen_sub = subtitles[0]
            for s in subtitles:
                if 'zh' in s.get('lan', '') or '中' in s.get('lan_doc', ''):
                    chosen_sub = s
                    break
            sub_url = chosen_sub.get('subtitle_url')
            if sub_url:
                if sub_url.startswith('//'):
                    sub_url = 'https:' + sub_url
                sub_content = fetch_json(sub_url)
                body = sub_content.get('body', [])
                txt_filename = os.path.join(output_dir, f"{safe_title}.subtitle.txt")
                with open(txt_filename, 'w', encoding='utf-8') as f:
                    f.write(f"# 视频标题: {video_title}\n# 分集: P{final_part} {part_title} ({format_seconds(duration)})\n\n")
                    for item in body:
                        t_from = item.get('from', 0)
                        t_to = item.get('to', 0)
                        text = item.get('content', '').strip()
                        if text:
                            f.write(f"[{format_seconds(t_from)} - {format_seconds(t_to)}] {text}\n")
                res["has_subtitle"] = True
                res["extracted_type"] = "subtitle"
                res["output_file"] = os.path.abspath(txt_filename)
                rotate_cache_history(output_dir)
                return res

        if mode == 'sub-only':
            res["status"] = "failed"
            res["error"] = "该 B 站视频未开放字幕"
            return res

    # 4. 自动拉取 360P 标清流
    sys.stderr.write(f"[Info] B 站无字幕或指定视频模式，正在拉取 360P 标清流...\n")
    play_url_api = f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=16&fnval=0"
    play_data = fetch_json(play_url_api)
    if play_data.get('code') != 0:
        raise RuntimeError(f"获取视频流失败: {play_data.get('message')}")

    durls = play_data.get('data', {}).get('durl', [])
    if not durls:
        raise RuntimeError("未找到 360P 视频流下载地址")

    video_stream_url = durls[0]['url']
    video_filename = os.path.join(output_dir, f"{safe_title}.360p.mp4")
    download_bilibili_stream(video_stream_url, video_filename)

    res["has_subtitle"] = False
    res["extracted_type"] = "video_low"
    res["output_file"] = os.path.abspath(video_filename)
    res["file_size_mb"] = round(durls[0].get('size', 0) / 1024 / 1024, 2)
    rotate_cache_history(output_dir)
    return res

# ======================= 通用全网通道 =======================

def process_generic(url: str, target_part: int | None, mode: str, output_dir: str) -> dict:
    if not ensure_yt_dlp():
        raise RuntimeError("未能启动 yt-dlp，无法抓取外部视频网站内容")

    url_hash = str(abs(hash(url)))[:8]
    cached_file, cached_type = check_cached_output(output_dir, url_hash, prefer_subtitle=(mode != 'video-low'))
    if cached_file:
        sys.stderr.write(f"[缓存命中] 发现通用视频本地缓存，跳过重复下载: {os.path.basename(cached_file)}\n")
        rotate_cache_history(output_dir)
        return {
            "status": "success",
            "platform": "generic",
            "url": url,
            "cached": True,
            "has_subtitle": (cached_type == "subtitle"),
            "extracted_type": cached_type,
            "output_file": os.path.abspath(cached_file),
            "file_size_mb": round(os.path.getsize(cached_file) / 1024 / 1024, 2)
        }

    res = {
        "status": "success",
        "platform": "generic",
        "url": url,
        "title": "外部视频",
        "cached": False,
        "has_subtitle": False,
        "extracted_type": None,
        "output_file": None
    }

    base_cmd = [sys.executable, "-m", "yt_dlp", "--no-warnings"]
    if target_part:
        base_cmd.extend(["--playlist-items", str(target_part)])

    # 1. 字幕
    if mode in ['auto', 'sub-only']:
        sys.stderr.write("[Info] 正在检测该视频是否包含字幕/AI字幕...\n")
        sub_out_tmpl = os.path.join(output_dir, f"%(title).40s_{url_hash}.%(ext)s")
        sub_cmd = base_cmd + [
            "--write-sub", "--write-auto-sub",
            "--sub-lang", "zh-Hans,zh,en,zh-CN",
            "--skip-download",
            "--convert-subs", "srt",
            "-o", sub_out_tmpl,
            url
        ]
        subprocess.run(sub_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')

        downloaded_subs = glob.glob(os.path.join(output_dir, f"*{url_hash}*.srt")) + \
                          glob.glob(os.path.join(output_dir, f"*{url_hash}*.vtt"))
        if downloaded_subs:
            latest_sub = max(downloaded_subs, key=os.path.getmtime)
            res["has_subtitle"] = True
            res["extracted_type"] = "subtitle"
            res["output_file"] = os.path.abspath(latest_sub)
            rotate_cache_history(output_dir)
            return res

        if mode == 'sub-only':
            res["status"] = "failed"
            res["error"] = "该视频未检索到可用字幕"
            return res

    # 2. 标清视频
    sys.stderr.write("[Info] 无可用字幕，正在下载标清压缩视频 (360P/480P)...\n")
    video_out_tmpl = os.path.join(output_dir, f"%(title).40s_{url_hash}_low.%(ext)s")
    video_cmd = base_cmd + [
        "-f", "worstvideo[ext=mp4]+worstaudio/worst[ext=mp4]/worst",
        "-o", video_out_tmpl,
        url
    ]
    subprocess.run(video_cmd, check=True)

    downloaded_videos = [
        os.path.join(output_dir, f) for f in os.listdir(output_dir)
        if url_hash in f and f.endswith(('.mp4', '.mkv', '.webm', '.flv'))
    ]
    if downloaded_videos:
        latest_video = max(downloaded_videos, key=os.path.getmtime)
        res["has_subtitle"] = False
        res["extracted_type"] = "video_low"
        res["output_file"] = os.path.abspath(latest_video)
        res["file_size_mb"] = round(os.path.getsize(latest_video) / 1024 / 1024, 2)
        rotate_cache_history(output_dir)
        return res

    raise RuntimeError("未能成功下载视频文件")

# ======================= 主入口调度 =======================

def is_direct_media_url(url: str) -> bool:
    clean_url = url.split('?')[0].lower()
    return clean_url.endswith(('.mp4', '.m4a', '.mp3', '.webm', '.flv', '.m3u8', '.mov'))

def process_direct_media(url: str, output_dir: str) -> dict:
    filename = url.split('?')[0].split('/')[-1]
    if not filename:
        filename = "direct_media.mp4"
    output_path = os.path.join(output_dir, filename)

    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        sys.stderr.write(f"[缓存命中] 发现直链媒体本地缓存: {filename}\n")
        os.utime(output_path, None)
        rotate_cache_history(output_dir)
        return {
            "status": "success",
            "platform": "direct_url",
            "title": filename,
            "cached": True,
            "has_subtitle": False,
            "extracted_type": "video_low",
            "output_file": os.path.abspath(output_path),
            "file_size_mb": round(os.path.getsize(output_path) / 1024 / 1024, 2)
        }

    sys.stderr.write(f"[Info] 检测到媒体直链，正在直接下载: {filename}...\n")
    download_bilibili_stream(url, output_path)
    rotate_cache_history(output_dir)
    return {
        "status": "success",
        "platform": "direct_url",
        "title": filename,
        "cached": False,
        "has_subtitle": False,
        "extracted_type": "video_low",
        "output_file": os.path.abspath(output_path),
        "file_size_mb": round(os.path.getsize(output_path) / 1024 / 1024, 2)
    }

def main():
    parser = argparse.ArgumentParser(description="全网视频字幕与标清流提取工具 (支持 B站, YouTube, 抖音等)")
    parser.add_argument("url", help="视频链接或 BV 号")
    parser.add_argument("-p", "--part", type=int, default=None, help="指定分P或列表项序号")
    parser.add_argument("-m", "--mode", choices=["auto", "sub-only", "video-low"], default="auto",
                        help="模式: auto (优先字幕, 无字幕下载标清流), sub-only (仅字幕), video-low (强制标清视频)")
    parser.add_argument("-o", "--output-dir", default=DEFAULT_CACHE_DIR,
                        help=f"输出缓存目录 (默认全局统一位置: {DEFAULT_CACHE_DIR})")
    parser.add_argument("--max-history", type=int, default=MAX_HISTORY_COUNT,
                        help=f"最多保留的最近历史任务数 (默认: {MAX_HISTORY_COUNT})")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    target_url = args.url.strip()
    is_bilibili = 'bilibili.com' in target_url or 'b23.tv' in target_url or target_url.startswith('BV')

    try:
        if is_bilibili:
            result = process_bilibili(target_url, args.part, args.mode, args.output_dir)
        elif is_direct_media_url(target_url):
            result = process_direct_media(target_url, args.output_dir)
        else:
            result = process_generic(target_url, args.part, args.mode, args.output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        err_res = {
            "status": "error",
            "message": str(e)
        }
        print(json.dumps(err_res, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
