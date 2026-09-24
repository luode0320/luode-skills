# 代码审查路径→规则映射

本文件描述了不同文件扩展名应匹配的审查规则文件，源自阿里巴巴 Open Code Review 的 system_rules.json。

## 使用方式

当审查系统检测到改动文件时：
1. 取文件相对于项目根的路径
2. 按下方顺序匹配最具体的 glob 模式
3. 加载对应的规则文件进行审查

## 规则映射

| 文件匹配模式 | 对应规则文件 | 说明 |
|------------|------------|------|
| `**/*.go` | go.md | Go 语言 |
| `**/*.{ts,js,tsx,jsx,mjs,cjs}` | ts_js_tsx_jsx.md | TypeScript / JavaScript |
| `**/*.java` | java.md | Java 语言 |
| `**/*.{py,pyi,ipynb}` | python.md | Python 语言 |
| `**/*.rs` | rust.md | Rust 语言 |
| `**/*.{kt,kts}` | kotlin.md | Kotlin 语言 |
| `**/*.{cpp,cc,cxx,hpp,hxx}` | cpp.md | C++ 语言 |
| `**/*.c` | c.md | C 语言 |
| `**/*.{php,phtml}` | php.md | PHP 语言 |
| `**/*.swift` | swift.md | Swift 语言 |
| `**/*.{fs,fsi,fsx}` | fsharp.md | F# 语言 |
| `**/*.{hbs,mustache}` | handlebars_mustache.md | Handlebars / Mustache 模板 |
| `**/*.{ftl,ftlh,ftlx}` | freemarker.md | FreeMarker 模板 |
| `**/*.pug` | pug.md | Pug 模板 |
| `**/*.ets` | arkts.md | ArkTS (鸿蒙) |
| `**/*.astro` | astro.md | Astro 框架 |
| `**/*.elm` | elm.md | Elm 语言 |
| `**/*.jl` | julia.md | Julia 语言 |
| `**/*.R` | r.md | R 语言 |
| `**/*.{hs,lhs}` | haskell.md | Haskell 语言 |
| `**/*.{nim,nims,nimble}` | nim.md | Nim 语言 |
| `**/*.zig` | zig.md | Zig 语言 |
| `**/*.sol` | solidity.md | Solidity 语言 |
| `**/*.vy` | vyper.md | Vyper 语言 |
| `**/*.rego` | rego.md | Rego (OPA) |
| `**/*.bicep` | bicep.md | Bicep (Azure) |
| `**/*.{tf,hcl,tfvars}` | terraform.md | Terraform / HCL |
| `**/*.nix` | nix.md | Nix 语言 |
| `**/*.{json,json5}` | json.md | JSON 文件 |
| `**/*.{yaml,yml}` | yaml.md | YAML 文件（非 GitHub 特殊目录） |
| `.github/workflows/**/*.{yaml,yml}` | github_workflows.md | GitHub Actions 工作流 |
| `.github/**/*.{yaml,yml}` | github_config.md | GitHub 配置文件 |
| `**/*.{v,sv,vh}` | verilog.md | Verilog (硬件描述) |
| `**/*.{vhd,vhdl}` | vhdl.md | VHDL (硬件描述) |
| `**/*.m` | matlab.md | MATLAB（若第一行匹配 ObjC 特征则改为 objc.md） |
| `**/*.mm` | objc.md | Objective-C |
| `**/*.{ml,mli}` | ocaml.md | OCaml 语言 |
| `**/*.{re,rei}` | ocaml.md | ReasonML (映射到 OCaml 规则) |
| `**/*.thrift` | thrift.md | Thrift IDL |
| `**/*.capnp` | capnp.md | Cap'n Proto |
| `**/*.proto` | protobuf.md | Protocol Buffers |
| `**/*.prisma` | prisma.md | Prisma ORM 模型 |
| `**/*.{graphql,gql}` | graphql.md | GraphQL |
| `**/*.jsonnet` | jsonnet.md | Jsonnet (配置模板) |
| `**/*{mapper,dao}*.xml` | mapper_dao_xml.md | MyBatis Mapper/DAO XML |
| `**/pom.xml` | pom_xml.md | Maven POM 配置 |
| `**/build.gradle` | build_gradle.md | Gradle 构建配置 |
| `**/package.json` | package_json.md | npm 包配置 |
| `**/Cargo.toml` | cargo_toml.md | Rust Cargo 配置 |
| `**/composer.json` | composer_json.md | PHP Composer 配置 |
| `**/*.properties` | properties.md | Properties 配置 |
| `**/*.po` | po.md | GNU gettext PO 文件 |
| `**/*.pot` | pot.md | GNU gettext POT 模板 |
| 其他/未匹配 | default.md | 通用规则 |

> 注意：`.m` 扩展名同时用于 MATLAB 和 Objective-C。系统通过扫描文件第一行进行嗅探：如果首行以 `#import`、`#include`、`@interface`、`//` 等 ObjC 特征开头，自动切换到 objc.md 规则。
