# 目录用法入口升级：测试 README

## 测试目的

验证 package-structure-rules 的目录用法索引模块（guide 子命令、Catalog 元数据字段、recipe 索引）正确工作。

## 测试对象

- package-structure-rules/references/placement-catalog.yaml（Catalog 扩展）
- package-structure-rules/scripts/placement_catalog.py（guide 子命令）
- package-structure-rules/references/usage-recipes-go.md（recipe 文档）

## 真实测试资产入口

- test/package-structure-rules/backend_utils_usage_routing_test.py

## 测试用例

| 测试 ID | 覆盖内容 | 入口 |
| --- | --- | --- |
| TC-1 | guide --category time 返回 timeUtil | backend_utils_usage_routing_test.py::test_guide_returns_time_util_recipe |
| TC-2 | guide --category conversion 返回 utils/convert | backend_utils_usage_routing_test.py::test_guide_returns_conversion_recipe |
| TC-3 | guide --category cache --technology redis 返回 utils/cache/redis | backend_utils_usage_routing_test.py::test_guide_returns_cache_redis_recipe |
| TC-4 | 所有 utils 条目有 related_skills | backend_utils_usage_routing_test.py::test_guide_all_util_entries_have_related_skills |
| TC-5 | backend-util-layout.md 与 Catalog 一致性 | backend_utils_usage_routing_test.py::test_backend_util_layout_consistency |

## 执行方式

```bash
python -X utf8 -m unittest discover -s test/package-structure-rules -p backend_utils_usage_routing_test.py -v
```

## 测试结果

5/5 通过。

## 结论

通过
