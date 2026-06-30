#!/usr/bin/env python3
"""
上线前接口测试计划生成脚本
功能：根据项目接口基线和本次上线改动范围，自动生成必测接口清单
"""
import argparse
import yaml
import os
from typing import List, Dict

def load_interface_inventory(inventory_path: str) -> List[Dict]:
    """加载接口基线文件"""
    if not os.path.exists(inventory_path):
        raise FileNotFoundError(f"接口基线文件不存在：{inventory_path}")
    with open(inventory_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or []

def filter_test_interfaces(inventory: List[Dict], changed_modules: List[str], include_p2: bool = False) -> Dict:
    """根据改动模块和风险等级筛选必测接口"""
    p0_list = []
    p1_list = []
    p2_list = []
    skipped_list = []

    for interface in inventory:
        risk_level = interface.get('风险等级', 'P2')
        module = interface.get('所属模块', '')
        must_test = interface.get('是否上线必测', '否') == '是'

        # P0级接口必测，无例外
        if risk_level == 'P0':
            p0_list.append(interface)
            continue
        
        # P1级接口，属于改动模块或关联模块的必测
        if risk_level == 'P1':
            if module in changed_modules or must_test:
                p1_list.append(interface)
            else:
                skipped_list.append({"接口": interface['接口标识'], "理由": "非改动模块P1接口，本次跳过"})
            continue
        
        # P2级接口，只有指定include_p2时才筛选改动模块的
        if risk_level == 'P2':
            if include_p2 and (module in changed_modules or must_test):
                p2_list.append(interface)
            else:
                skipped_list.append({"接口": interface['接口标识'], "理由": "非改动模块P2接口，本次跳过"})
            continue
    
    # 整理结果
    result = {
        "summary": {
            "总接口数": len(inventory),
            "必测P0接口数": len(p0_list),
            "必测P1接口数": len(p1_list),
            "必测P2接口数": len(p2_list),
            "跳过接口数": len(skipped_list),
            "本次改动模块": changed_modules
        },
        "p0_interfaces": p0_list,
        "p1_interfaces": p1_list,
        "p2_interfaces": p2_list,
        "skipped_interfaces": skipped_list
    }
    return result

def save_test_plan(test_plan: Dict, output_path: str):
    """保存测试计划到文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(test_plan, f, allow_unicode=True, sort_keys=False)
    print(f"测试计划已生成：{output_path}")
    print(f"必测P0接口：{test_plan['summary']['必测P0接口数']} 个")
    print(f"必测P1接口：{test_plan['summary']['必测P1接口数']} 个")
    print(f"必测P2接口：{test_plan['summary']['必测P2接口数']} 个")
    print(f"跳过接口：{test_plan['summary']['跳过接口数']} 个")

def main():
    parser = argparse.ArgumentParser(description="上线前接口测试计划生成工具")
    parser.add_argument("--inventory", required=True, help="接口基线文件路径，YAML格式")
    parser.add_argument("--modules", required=True, nargs="+", help="本次上线改动的模块列表，空格分隔")
    parser.add_argument("--include-p2", action="store_true", help="是否包含改动模块的P2接口，默认不包含")
    parser.add_argument("--output", default="release-test-plan.yaml", help="输出测试计划文件路径，默认当前目录release-test-plan.yaml")
    args = parser.parse_args()

    # 加载基线
    inventory = load_interface_inventory(args.inventory)
    # 筛选接口
    test_plan = filter_test_interfaces(inventory, args.modules, args.include_p2)
    # 保存结果
    save_test_plan(test_plan, args.output)

if __name__ == "__main__":
    main()
