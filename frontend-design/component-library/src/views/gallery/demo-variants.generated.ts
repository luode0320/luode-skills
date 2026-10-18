/* 由 scripts/build_demo_variants.mjs 从组件公开契约机械派生，禁止手改；
   重新生成命令：node scripts/build_demo_variants.mjs
   每项是「基础示例之外的一组可用示例」，标签用契约语言写明差异点。 */
export interface GeneratedVariant {
  /** 变体标签：直接呈现为示例卡上的差异说明 */
  label: string
  /** 覆盖基础示例的 props 片段 */
  props: Record<string, unknown>
  /** 派生来源：enum / boolean / number */
  source: string
}

export const GENERATED_VARIANTS: Record<string, GeneratedVariant[]> = {
  "Icon": [
    {
      "label": "size=16",
      "props": {
        "size": 16
      },
      "source": "number"
    },
    {
      "label": "size=28",
      "props": {
        "size": 28
      },
      "source": "number"
    },
    {
      "label": "size=44",
      "props": {
        "size": 44
      },
      "source": "number"
    }
  ],
  "NeuralNet": [],
  "AskDock": [
    {
      "label": "开启 compact",
      "props": {
        "compact": true
      },
      "source": "boolean"
    }
  ],
  "BoardView": [
    {
      "label": "关闭 draggable",
      "props": {
        "draggable": false
      },
      "source": "boolean"
    }
  ],
  "DeptSelect": [
    {
      "label": "开启 invalid",
      "props": {
        "invalid": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 clearable",
      "props": {
        "clearable": true
      },
      "source": "boolean"
    }
  ],
  "DeptTree": [],
  "DictSelect": [
    {
      "label": "开启 invalid",
      "props": {
        "invalid": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "DictSwatchbook": [
    {
      "label": "开启 loading",
      "props": {
        "loading": true
      },
      "source": "boolean"
    }
  ],
  "DictTag": [],
  "FormDialog": [
    {
      "label": "width=480",
      "props": {
        "width": 480
      },
      "source": "number"
    },
    {
      "label": "width=760",
      "props": {
        "width": 760
      },
      "source": "number"
    }
  ],
  "GeneratorPipeline": [],
  "InsightPanel": [],
  "ListPage": [
    {
      "label": "开启 selectable",
      "props": {
        "selectable": true
      },
      "source": "boolean"
    }
  ],
  "MenuStarMap": [],
  "OrgCanvas": [],
  "PermissionButton": [
    {
      "label": "variant=secondary",
      "props": {
        "variant": "secondary"
      },
      "source": "enum"
    },
    {
      "label": "variant=ghost",
      "props": {
        "variant": "ghost"
      },
      "source": "enum"
    },
    {
      "label": "variant=text",
      "props": {
        "variant": "text"
      },
      "source": "enum"
    },
    {
      "label": "variant=danger",
      "props": {
        "variant": "danger"
      },
      "source": "enum"
    },
    {
      "label": "size=sm",
      "props": {
        "size": "sm"
      },
      "source": "enum"
    },
    {
      "label": "开启 loading",
      "props": {
        "loading": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "PermissionMatrix": [
    {
      "label": "关闭 editable",
      "props": {
        "editable": false
      },
      "source": "boolean"
    }
  ],
  "PermissionTrace": [],
  "PermissionTree": [],
  "PostLadder": [
    {
      "label": "开启 loading",
      "props": {
        "loading": true
      },
      "source": "boolean"
    }
  ],
  "SearchForm": [
    {
      "label": "开启 loading",
      "props": {
        "loading": true
      },
      "source": "boolean"
    }
  ],
  "UserSelect": [
    {
      "label": "valueKey=nickname",
      "props": {
        "valueKey": "nickname"
      },
      "source": "enum"
    },
    {
      "label": "关闭 clearable",
      "props": {
        "clearable": false
      },
      "source": "boolean"
    }
  ],
  "BarChart": [
    {
      "label": "height=120",
      "props": {
        "height": 120
      },
      "source": "number"
    },
    {
      "label": "height=200",
      "props": {
        "height": 200
      },
      "source": "number"
    },
    {
      "label": "height=280",
      "props": {
        "height": 280
      },
      "source": "number"
    }
  ],
  "HeatGrid": [
    {
      "label": "开启 loading",
      "props": {
        "loading": true
      },
      "source": "boolean"
    }
  ],
  "RelationGraph": [
    {
      "label": "variant=stage",
      "props": {
        "variant": "stage"
      },
      "source": "enum"
    }
  ],
  "Swimlane": [
    {
      "label": "开启 compact",
      "props": {
        "compact": true
      },
      "source": "boolean"
    }
  ],
  "TickRing": [
    {
      "label": "display=2",
      "props": {
        "display": 2
      },
      "source": "number"
    },
    {
      "label": "display=6",
      "props": {
        "display": 6
      },
      "source": "number"
    },
    {
      "label": "size=16",
      "props": {
        "size": 16
      },
      "source": "number"
    },
    {
      "label": "size=28",
      "props": {
        "size": 28
      },
      "source": "number"
    },
    {
      "label": "size=44",
      "props": {
        "size": 44
      },
      "source": "number"
    },
    {
      "label": "ticks=24",
      "props": {
        "ticks": 24
      },
      "source": "number"
    },
    {
      "label": "ticks=72",
      "props": {
        "ticks": 72
      },
      "source": "number"
    }
  ],
  "TrendChart": [
    {
      "label": "height=120",
      "props": {
        "height": 120
      },
      "source": "number"
    },
    {
      "label": "height=200",
      "props": {
        "height": 200
      },
      "source": "number"
    },
    {
      "label": "height=280",
      "props": {
        "height": 280
      },
      "source": "number"
    },
    {
      "label": "关闭 dots",
      "props": {
        "dots": false
      },
      "source": "boolean"
    },
    {
      "label": "tone=ink",
      "props": {
        "tone": "ink"
      },
      "source": "enum"
    }
  ],
  "Affix": [
    {
      "label": "offsetTop=24",
      "props": {
        "offsetTop": 24
      },
      "source": "number"
    },
    {
      "label": "offsetTop=80",
      "props": {
        "offsetTop": 80
      },
      "source": "number"
    }
  ],
  "Alert": [
    {
      "label": "type=success",
      "props": {
        "type": "success"
      },
      "source": "enum"
    },
    {
      "label": "type=warning",
      "props": {
        "type": "warning"
      },
      "source": "enum"
    },
    {
      "label": "type=error",
      "props": {
        "type": "error"
      },
      "source": "enum"
    },
    {
      "label": "关闭 closable",
      "props": {
        "closable": false
      },
      "source": "boolean"
    },
    {
      "label": "关闭 showIcon",
      "props": {
        "showIcon": false
      },
      "source": "boolean"
    }
  ],
  "Anchor": [],
  "AutoComplete": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 clearable",
      "props": {
        "clearable": true
      },
      "source": "boolean"
    }
  ],
  "AvatarGroup": [
    {
      "label": "size=16",
      "props": {
        "size": 16
      },
      "source": "number"
    },
    {
      "label": "size=28",
      "props": {
        "size": 28
      },
      "source": "number"
    },
    {
      "label": "size=44",
      "props": {
        "size": 44
      },
      "source": "number"
    },
    {
      "label": "total=3",
      "props": {
        "total": 3
      },
      "source": "number"
    },
    {
      "label": "total=8",
      "props": {
        "total": 8
      },
      "source": "number"
    }
  ],
  "BackTop": [],
  "Badge": [
    {
      "label": "开启 dot",
      "props": {
        "dot": true
      },
      "source": "boolean"
    },
    {
      "label": "tone=info",
      "props": {
        "tone": "info"
      },
      "source": "enum"
    },
    {
      "label": "tone=ok",
      "props": {
        "tone": "ok"
      },
      "source": "enum"
    },
    {
      "label": "tone=neutral",
      "props": {
        "tone": "neutral"
      },
      "source": "enum"
    }
  ],
  "Breadcrumb": [],
  "ButtonGroup": [
    {
      "label": "size=sm",
      "props": {
        "size": "sm"
      },
      "source": "enum"
    },
    {
      "label": "direction=vertical",
      "props": {
        "direction": "vertical"
      },
      "source": "enum"
    }
  ],
  "Calendar": [
    {
      "label": "mode=year",
      "props": {
        "mode": "year"
      },
      "source": "enum"
    }
  ],
  "Card": [
    {
      "label": "关闭 bordered",
      "props": {
        "bordered": false
      },
      "source": "boolean"
    },
    {
      "label": "关闭 hoverable",
      "props": {
        "hoverable": false
      },
      "source": "boolean"
    },
    {
      "label": "开启 loading",
      "props": {
        "loading": true
      },
      "source": "boolean"
    }
  ],
  "CardGrid": [
    {
      "label": "columns=3",
      "props": {
        "columns": 3
      },
      "source": "number"
    },
    {
      "label": "columns=4",
      "props": {
        "columns": 4
      },
      "source": "number"
    },
    {
      "label": "gutter=8",
      "props": {
        "gutter": 8
      },
      "source": "number"
    },
    {
      "label": "gutter=24",
      "props": {
        "gutter": 24
      },
      "source": "number"
    }
  ],
  "CardMeta": [],
  "Carousel": [
    {
      "label": "关闭 loop",
      "props": {
        "loop": false
      },
      "source": "boolean"
    },
    {
      "label": "indicatorPosition=outside",
      "props": {
        "indicatorPosition": "outside"
      },
      "source": "enum"
    },
    {
      "label": "indicatorPosition=none",
      "props": {
        "indicatorPosition": "none"
      },
      "source": "enum"
    },
    {
      "label": "showArrow=always",
      "props": {
        "showArrow": "always"
      },
      "source": "enum"
    },
    {
      "label": "showArrow=never",
      "props": {
        "showArrow": "never"
      },
      "source": "enum"
    }
  ],
  "Cascader": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 clearable",
      "props": {
        "clearable": true
      },
      "source": "boolean"
    }
  ],
  "CascaderPanel": [
    {
      "label": "columnWidth=100",
      "props": {
        "columnWidth": 100
      },
      "source": "number"
    },
    {
      "label": "columnWidth=180",
      "props": {
        "columnWidth": 180
      },
      "source": "number"
    }
  ],
  "CheckboxGroup": [
    {
      "label": "direction=vertical",
      "props": {
        "direction": "vertical"
      },
      "source": "enum"
    }
  ],
  "Collapse": [
    {
      "label": "开启 bordered",
      "props": {
        "bordered": true
      },
      "source": "boolean"
    },
    {
      "label": "expandIconPosition=right",
      "props": {
        "expandIconPosition": "right"
      },
      "source": "enum"
    }
  ],
  "CollapseItem": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "ColorPicker": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "关闭 showText",
      "props": {
        "showText": false
      },
      "source": "boolean"
    }
  ],
  "Comment": [],
  "Countdown": [],
  "DataList": [
    {
      "label": "关闭 bordered",
      "props": {
        "bordered": false
      },
      "source": "boolean"
    },
    {
      "label": "size=sm",
      "props": {
        "size": "sm"
      },
      "source": "enum"
    },
    {
      "label": "size=lg",
      "props": {
        "size": "lg"
      },
      "source": "enum"
    },
    {
      "label": "关闭 split",
      "props": {
        "split": false
      },
      "source": "boolean"
    },
    {
      "label": "开启 loading",
      "props": {
        "loading": true
      },
      "source": "boolean"
    }
  ],
  "DatePicker": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 clearable",
      "props": {
        "clearable": true
      },
      "source": "boolean"
    }
  ],
  "Descriptions": [
    {
      "label": "关闭 bordered",
      "props": {
        "bordered": false
      },
      "source": "boolean"
    },
    {
      "label": "layout=vertical",
      "props": {
        "layout": "vertical"
      },
      "source": "enum"
    }
  ],
  "Divider": [
    {
      "label": "orientation=left",
      "props": {
        "orientation": "left"
      },
      "source": "enum"
    },
    {
      "label": "orientation=right",
      "props": {
        "orientation": "right"
      },
      "source": "enum"
    }
  ],
  "Dropdown": [
    {
      "label": "trigger=hover",
      "props": {
        "trigger": "hover"
      },
      "source": "enum"
    },
    {
      "label": "placement=top",
      "props": {
        "placement": "top"
      },
      "source": "enum"
    }
  ],
  "DropdownButton": [
    {
      "label": "type=secondary",
      "props": {
        "type": "secondary"
      },
      "source": "enum"
    },
    {
      "label": "type=ghost",
      "props": {
        "type": "ghost"
      },
      "source": "enum"
    },
    {
      "label": "type=text",
      "props": {
        "type": "text"
      },
      "source": "enum"
    },
    {
      "label": "type=danger",
      "props": {
        "type": "danger"
      },
      "source": "enum"
    }
  ],
  "DropdownSubmenu": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "Form": [
    {
      "label": "layout=inline",
      "props": {
        "layout": "inline"
      },
      "source": "enum"
    }
  ],
  "GridCol": [
    {
      "label": "span=6",
      "props": {
        "span": 6
      },
      "source": "number"
    },
    {
      "label": "span=24",
      "props": {
        "span": 24
      },
      "source": "number"
    }
  ],
  "GridRow": [
    {
      "label": "justify=center",
      "props": {
        "justify": "center"
      },
      "source": "enum"
    },
    {
      "label": "justify=end",
      "props": {
        "justify": "end"
      },
      "source": "enum"
    },
    {
      "label": "justify=space-between",
      "props": {
        "justify": "space-between"
      },
      "source": "enum"
    },
    {
      "label": "justify=space-around",
      "props": {
        "justify": "space-around"
      },
      "source": "enum"
    },
    {
      "label": "align=start",
      "props": {
        "align": "start"
      },
      "source": "enum"
    },
    {
      "label": "align=center",
      "props": {
        "align": "center"
      },
      "source": "enum"
    },
    {
      "label": "align=end",
      "props": {
        "align": "end"
      },
      "source": "enum"
    },
    {
      "label": "关闭 wrap",
      "props": {
        "wrap": false
      },
      "source": "boolean"
    }
  ],
  "HelpTip": [
    {
      "label": "tone=help",
      "props": {
        "tone": "help"
      },
      "source": "enum"
    },
    {
      "label": "placement=bottom",
      "props": {
        "placement": "bottom"
      },
      "source": "enum"
    },
    {
      "label": "placement=left",
      "props": {
        "placement": "left"
      },
      "source": "enum"
    },
    {
      "label": "placement=right",
      "props": {
        "placement": "right"
      },
      "source": "enum"
    },
    {
      "label": "size=16",
      "props": {
        "size": 16
      },
      "source": "number"
    },
    {
      "label": "size=28",
      "props": {
        "size": 28
      },
      "source": "number"
    },
    {
      "label": "size=44",
      "props": {
        "size": 44
      },
      "source": "number"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "Image": [
    {
      "label": "fit=fill",
      "props": {
        "fit": "fill"
      },
      "source": "enum"
    },
    {
      "label": "fit=contain",
      "props": {
        "fit": "contain"
      },
      "source": "enum"
    },
    {
      "label": "fit=none",
      "props": {
        "fit": "none"
      },
      "source": "enum"
    },
    {
      "label": "fit=scale-down",
      "props": {
        "fit": "scale-down"
      },
      "source": "enum"
    },
    {
      "label": "关闭 preview",
      "props": {
        "preview": false
      },
      "source": "boolean"
    }
  ],
  "ImagePreview": [],
  "ImagePreviewGroup": [
    {
      "label": "initialIndex=1",
      "props": {
        "initialIndex": 1
      },
      "source": "number"
    },
    {
      "label": "initialIndex=2",
      "props": {
        "initialIndex": 2
      },
      "source": "number"
    }
  ],
  "InputGroup": [
    {
      "label": "direction=vertical",
      "props": {
        "direction": "vertical"
      },
      "source": "enum"
    }
  ],
  "InputNumber": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "InputPassword": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "InputSearch": [
    {
      "label": "开启 loading",
      "props": {
        "loading": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "关闭 allowClear",
      "props": {
        "allowClear": false
      },
      "source": "boolean"
    }
  ],
  "InputTag": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "LinkText": [
    {
      "label": "target=_blank",
      "props": {
        "target": "_blank"
      },
      "source": "enum"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 underline",
      "props": {
        "underline": true
      },
      "source": "boolean"
    },
    {
      "label": "type=default",
      "props": {
        "type": "default"
      },
      "source": "enum"
    },
    {
      "label": "type=success",
      "props": {
        "type": "success"
      },
      "source": "enum"
    },
    {
      "label": "type=warning",
      "props": {
        "type": "warning"
      },
      "source": "enum"
    },
    {
      "label": "type=danger",
      "props": {
        "type": "danger"
      },
      "source": "enum"
    }
  ],
  "Mention": [
    {
      "label": "rows=2",
      "props": {
        "rows": 2
      },
      "source": "number"
    },
    {
      "label": "rows=5",
      "props": {
        "rows": 5
      },
      "source": "number"
    }
  ],
  "Menu": [
    {
      "label": "mode=horizontal",
      "props": {
        "mode": "horizontal"
      },
      "source": "enum"
    }
  ],
  "MenuNode": [],
  "MonthPicker": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "关闭 clearable",
      "props": {
        "clearable": false
      },
      "source": "boolean"
    }
  ],
  "Notification": [
    {
      "label": "type=info",
      "props": {
        "type": "info"
      },
      "source": "enum"
    },
    {
      "label": "type=warning",
      "props": {
        "type": "warning"
      },
      "source": "enum"
    },
    {
      "label": "type=error",
      "props": {
        "type": "error"
      },
      "source": "enum"
    },
    {
      "label": "关闭 closable",
      "props": {
        "closable": false
      },
      "source": "boolean"
    },
    {
      "label": "关闭 showIcon",
      "props": {
        "showIcon": false
      },
      "source": "boolean"
    }
  ],
  "OverflowList": [
    {
      "label": "collapseFrom=start",
      "props": {
        "collapseFrom": "start"
      },
      "source": "enum"
    }
  ],
  "Popconfirm": [
    {
      "label": "关闭 danger",
      "props": {
        "danger": false
      },
      "source": "boolean"
    },
    {
      "label": "placement=bottom",
      "props": {
        "placement": "bottom"
      },
      "source": "enum"
    },
    {
      "label": "placement=left",
      "props": {
        "placement": "left"
      },
      "source": "enum"
    },
    {
      "label": "placement=right",
      "props": {
        "placement": "right"
      },
      "source": "enum"
    }
  ],
  "Popover": [
    {
      "label": "trigger=click",
      "props": {
        "trigger": "click"
      },
      "source": "enum"
    },
    {
      "label": "placement=bottom",
      "props": {
        "placement": "bottom"
      },
      "source": "enum"
    },
    {
      "label": "placement=left",
      "props": {
        "placement": "left"
      },
      "source": "enum"
    },
    {
      "label": "placement=right",
      "props": {
        "placement": "right"
      },
      "source": "enum"
    },
    {
      "label": "width=120",
      "props": {
        "width": 120
      },
      "source": "number"
    },
    {
      "label": "width=320",
      "props": {
        "width": 320
      },
      "source": "number"
    }
  ],
  "Progress": [
    {
      "label": "percent=25",
      "props": {
        "percent": 25
      },
      "source": "number"
    },
    {
      "label": "percent=80",
      "props": {
        "percent": 80
      },
      "source": "number"
    },
    {
      "label": "type=circle",
      "props": {
        "type": "circle"
      },
      "source": "enum"
    },
    {
      "label": "status=success",
      "props": {
        "status": "success"
      },
      "source": "enum"
    },
    {
      "label": "status=error",
      "props": {
        "status": "error"
      },
      "source": "enum"
    },
    {
      "label": "status=warning",
      "props": {
        "status": "warning"
      },
      "source": "enum"
    },
    {
      "label": "size=16",
      "props": {
        "size": 16,
        "type": "circle"
      },
      "source": "number"
    },
    {
      "label": "size=28",
      "props": {
        "size": 28,
        "type": "circle"
      },
      "source": "number"
    },
    {
      "label": "size=44",
      "props": {
        "size": 44,
        "type": "circle"
      },
      "source": "number"
    },
    {
      "label": "关闭 showText",
      "props": {
        "showText": false
      },
      "source": "boolean"
    }
  ],
  "QuarterPicker": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "关闭 clearable",
      "props": {
        "clearable": false
      },
      "source": "boolean"
    }
  ],
  "Radio": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "RadioGroup": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "direction=vertical",
      "props": {
        "direction": "vertical"
      },
      "source": "enum"
    }
  ],
  "RangePicker": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "关闭 clearable",
      "props": {
        "clearable": false
      },
      "source": "boolean"
    }
  ],
  "Rate": [
    {
      "label": "count=3",
      "props": {
        "count": 3
      },
      "source": "number"
    },
    {
      "label": "count=8",
      "props": {
        "count": 8
      },
      "source": "number"
    },
    {
      "label": "开启 readonly",
      "props": {
        "readonly": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 allowClear",
      "props": {
        "allowClear": true
      },
      "source": "boolean"
    }
  ],
  "ResizeBox": [
    {
      "label": "direction=vertical",
      "props": {
        "direction": "vertical"
      },
      "source": "enum"
    },
    {
      "label": "width=120",
      "props": {
        "width": 120
      },
      "source": "number"
    },
    {
      "label": "width=240",
      "props": {
        "width": 240
      },
      "source": "number"
    },
    {
      "label": "width=320",
      "props": {
        "width": 320
      },
      "source": "number"
    },
    {
      "label": "height=120",
      "props": {
        "height": 120
      },
      "source": "number"
    },
    {
      "label": "height=200",
      "props": {
        "height": 200
      },
      "source": "number"
    },
    {
      "label": "height=280",
      "props": {
        "height": 280
      },
      "source": "number"
    }
  ],
  "Result": [
    {
      "label": "status=error",
      "props": {
        "status": "error"
      },
      "source": "enum"
    },
    {
      "label": "status=warning",
      "props": {
        "status": "warning"
      },
      "source": "enum"
    },
    {
      "label": "status=info",
      "props": {
        "status": "info"
      },
      "source": "enum"
    },
    {
      "label": "status=404",
      "props": {
        "status": "404"
      },
      "source": "enum"
    },
    {
      "label": "status=403",
      "props": {
        "status": "403"
      },
      "source": "enum"
    },
    {
      "label": "status=500",
      "props": {
        "status": "500"
      },
      "source": "enum"
    }
  ],
  "Skeleton": [
    {
      "label": "rows=2",
      "props": {
        "rows": 2
      },
      "source": "number"
    },
    {
      "label": "rows=5",
      "props": {
        "rows": 5
      },
      "source": "number"
    },
    {
      "label": "type=image",
      "props": {
        "type": "image"
      },
      "source": "enum"
    },
    {
      "label": "type=circle",
      "props": {
        "type": "circle"
      },
      "source": "enum"
    },
    {
      "label": "type=rect",
      "props": {
        "type": "rect"
      },
      "source": "enum"
    }
  ],
  "Slider": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "Space": [
    {
      "label": "direction=vertical",
      "props": {
        "direction": "vertical"
      },
      "source": "enum"
    },
    {
      "label": "size=sm",
      "props": {
        "size": "sm"
      },
      "source": "enum"
    },
    {
      "label": "size=lg",
      "props": {
        "size": "lg"
      },
      "source": "enum"
    },
    {
      "label": "align=start",
      "props": {
        "align": "start"
      },
      "source": "enum"
    },
    {
      "label": "align=end",
      "props": {
        "align": "end"
      },
      "source": "enum"
    },
    {
      "label": "align=baseline",
      "props": {
        "align": "baseline"
      },
      "source": "enum"
    },
    {
      "label": "开启 wrap",
      "props": {
        "wrap": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 split",
      "props": {
        "split": true
      },
      "source": "boolean"
    }
  ],
  "Spin": [
    {
      "label": "size=sm",
      "props": {
        "size": "sm"
      },
      "source": "enum"
    },
    {
      "label": "size=lg",
      "props": {
        "size": "lg"
      },
      "source": "enum"
    }
  ],
  "SplitPane": [
    {
      "label": "direction=vertical",
      "props": {
        "direction": "vertical"
      },
      "source": "enum"
    }
  ],
  "Steps": [
    {
      "label": "current=0",
      "props": {
        "current": 0
      },
      "source": "number"
    },
    {
      "label": "current=2",
      "props": {
        "current": 2
      },
      "source": "number"
    },
    {
      "label": "direction=vertical",
      "props": {
        "direction": "vertical"
      },
      "source": "enum"
    }
  ],
  "StyledScrollbar": [
    {
      "label": "direction=horizontal",
      "props": {
        "direction": "horizontal"
      },
      "source": "enum"
    }
  ],
  "TabPane": [],
  "Tabs": [
    {
      "label": "type=card",
      "props": {
        "type": "card"
      },
      "source": "enum"
    },
    {
      "label": "开启 closable",
      "props": {
        "closable": true
      },
      "source": "boolean"
    }
  ],
  "Textarea": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 readonly",
      "props": {
        "readonly": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 invalid",
      "props": {
        "invalid": true
      },
      "source": "boolean"
    },
    {
      "label": "rows=2",
      "props": {
        "rows": 2
      },
      "source": "number"
    },
    {
      "label": "rows=5",
      "props": {
        "rows": 5
      },
      "source": "number"
    }
  ],
  "TimePicker": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 clearable",
      "props": {
        "clearable": true
      },
      "source": "boolean"
    }
  ],
  "Timeline": [
    {
      "label": "mode=right",
      "props": {
        "mode": "right"
      },
      "source": "enum"
    },
    {
      "label": "mode=alternate",
      "props": {
        "mode": "alternate"
      },
      "source": "enum"
    }
  ],
  "TimelineItem": [],
  "Tooltip": [
    {
      "label": "placement=bottom",
      "props": {
        "placement": "bottom"
      },
      "source": "enum"
    },
    {
      "label": "placement=left",
      "props": {
        "placement": "left"
      },
      "source": "enum"
    },
    {
      "label": "placement=right",
      "props": {
        "placement": "right"
      },
      "source": "enum"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "Transfer": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "Tree": [
    {
      "label": "关闭 checkable",
      "props": {
        "checkable": false
      },
      "source": "boolean"
    },
    {
      "label": "关闭 selectable",
      "props": {
        "selectable": false
      },
      "source": "boolean"
    },
    {
      "label": "关闭 multiple",
      "props": {
        "multiple": false
      },
      "source": "boolean"
    },
    {
      "label": "关闭 showLine",
      "props": {
        "showLine": false
      },
      "source": "boolean"
    }
  ],
  "TreeNode": [],
  "TreeSelect": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 clearable",
      "props": {
        "clearable": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 multiple",
      "props": {
        "multiple": true,
        "modelValue": [
          11,
          12
        ]
      },
      "source": "boolean"
    }
  ],
  "Trigger": [
    {
      "label": "trigger=hover",
      "props": {
        "trigger": [
          "hover"
        ]
      },
      "source": "enum"
    },
    {
      "label": "trigger=focus",
      "props": {
        "trigger": [
          "focus"
        ]
      },
      "source": "enum"
    },
    {
      "label": "trigger=contextmenu",
      "props": {
        "trigger": [
          "contextmenu"
        ]
      },
      "source": "enum"
    },
    {
      "label": "placement=top",
      "props": {
        "placement": "top"
      },
      "source": "enum"
    },
    {
      "label": "placement=left",
      "props": {
        "placement": "left"
      },
      "source": "enum"
    },
    {
      "label": "placement=right",
      "props": {
        "placement": "right"
      },
      "source": "enum"
    },
    {
      "label": "placement=bottom-start",
      "props": {
        "placement": "bottom-start"
      },
      "source": "enum"
    },
    {
      "label": "placement=bottom-end",
      "props": {
        "placement": "bottom-end"
      },
      "source": "enum"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "Typography": [
    {
      "label": "type=text",
      "props": {
        "type": "text"
      },
      "source": "enum"
    },
    {
      "label": "type=paragraph",
      "props": {
        "type": "paragraph"
      },
      "source": "enum"
    },
    {
      "label": "开启 underline",
      "props": {
        "underline": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "Upload": [
    {
      "label": "开启 multiple",
      "props": {
        "multiple": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "VerificationCode": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 invalid",
      "props": {
        "invalid": true
      },
      "source": "boolean"
    }
  ],
  "Watermark": [],
  "WeekPicker": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "关闭 clearable",
      "props": {
        "clearable": false
      },
      "source": "boolean"
    }
  ],
  "YearPicker": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "关闭 clearable",
      "props": {
        "clearable": false
      },
      "source": "boolean"
    }
  ],
  "AppShell": [],
  "AppearanceDialog": [],
  "CommandPalette": [],
  "PasswordDialog": [],
  "Sidebar": [],
  "Topbar": [],
  "Avatar": [
    {
      "label": "size=16",
      "props": {
        "size": 16
      },
      "source": "number"
    },
    {
      "label": "size=28",
      "props": {
        "size": 28
      },
      "source": "number"
    },
    {
      "label": "size=44",
      "props": {
        "size": 44
      },
      "source": "number"
    }
  ],
  "Button": [
    {
      "label": "variant=primary",
      "props": {
        "variant": "primary"
      },
      "source": "enum"
    },
    {
      "label": "variant=ghost",
      "props": {
        "variant": "ghost"
      },
      "source": "enum"
    },
    {
      "label": "variant=text",
      "props": {
        "variant": "text"
      },
      "source": "enum"
    },
    {
      "label": "variant=danger",
      "props": {
        "variant": "danger"
      },
      "source": "enum"
    },
    {
      "label": "size=sm",
      "props": {
        "size": "sm"
      },
      "source": "enum"
    },
    {
      "label": "开启 loading",
      "props": {
        "loading": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "type=submit",
      "props": {
        "type": "submit"
      },
      "source": "enum"
    }
  ],
  "Checkbox": [
    {
      "label": "开启 indeterminate",
      "props": {
        "indeterminate": true,
        "modelValue": false
      },
      "source": "boolean"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "ConfirmHost": [],
  "DataTable": [
    {
      "label": "关闭 selectable",
      "props": {
        "selectable": false
      },
      "source": "boolean"
    },
    {
      "label": "开启 loading",
      "props": {
        "loading": true
      },
      "source": "boolean"
    }
  ],
  "DeltaPill": [],
  "Drawer": [
    {
      "label": "width=380",
      "props": {
        "width": 380
      },
      "source": "number"
    },
    {
      "label": "width=680",
      "props": {
        "width": 680
      },
      "source": "number"
    }
  ],
  "EmptyState": [],
  "Field": [],
  "HoverCard": [
    {
      "label": "placement=top",
      "props": {
        "placement": "top"
      },
      "source": "enum"
    },
    {
      "label": "width=120",
      "props": {
        "width": 120
      },
      "source": "number"
    },
    {
      "label": "width=240",
      "props": {
        "width": 240
      },
      "source": "number"
    },
    {
      "label": "width=320",
      "props": {
        "width": 320
      },
      "source": "number"
    }
  ],
  "IconButton": [
    {
      "label": "size=16",
      "props": {
        "size": 16
      },
      "source": "number"
    },
    {
      "label": "size=28",
      "props": {
        "size": 28
      },
      "source": "number"
    },
    {
      "label": "size=44",
      "props": {
        "size": 44
      },
      "source": "number"
    },
    {
      "label": "开启 bordered",
      "props": {
        "bordered": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "Metric": [
    {
      "label": "size=xl",
      "props": {
        "size": "xl"
      },
      "source": "enum"
    },
    {
      "label": "size=l",
      "props": {
        "size": "l"
      },
      "source": "enum"
    },
    {
      "label": "size=s",
      "props": {
        "size": "s"
      },
      "source": "enum"
    }
  ],
  "Modal": [
    {
      "label": "width=420",
      "props": {
        "width": 420
      },
      "source": "number"
    },
    {
      "label": "width=720",
      "props": {
        "width": 720
      },
      "source": "number"
    }
  ],
  "Odometer": [
    {
      "label": "关闭 group",
      "props": {
        "group": false
      },
      "source": "boolean"
    }
  ],
  "PageHeader": [],
  "Pagination": [
    {
      "label": "total=3",
      "props": {
        "total": 3
      },
      "source": "number"
    },
    {
      "label": "total=8",
      "props": {
        "total": 8
      },
      "source": "number"
    },
    {
      "label": "pageSize=5",
      "props": {
        "pageSize": 5
      },
      "source": "number"
    },
    {
      "label": "pageSize=20",
      "props": {
        "pageSize": 20
      },
      "source": "number"
    }
  ],
  "Panel": [],
  "Ruler": [],
  "SectionLabel": [
    {
      "label": "as=h3",
      "props": {
        "as": "h3"
      },
      "source": "enum"
    }
  ],
  "Segmented": [],
  "Select": [
    {
      "label": "开启 filterable",
      "props": {
        "filterable": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 clearable",
      "props": {
        "clearable": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 invalid",
      "props": {
        "invalid": true
      },
      "source": "boolean"
    }
  ],
  "SpecPlate": [],
  "StatusTag": [],
  "Switch": [
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    }
  ],
  "Tag": [
    {
      "label": "开启 dot",
      "props": {
        "dot": true
      },
      "source": "boolean"
    }
  ],
  "TextInput": [
    {
      "label": "type=password",
      "props": {
        "type": "password"
      },
      "source": "enum"
    },
    {
      "label": "type=number",
      "props": {
        "type": "number"
      },
      "source": "enum"
    },
    {
      "label": "type=email",
      "props": {
        "type": "email"
      },
      "source": "enum"
    },
    {
      "label": "type=tel",
      "props": {
        "type": "tel"
      },
      "source": "enum"
    },
    {
      "label": "开启 invalid",
      "props": {
        "invalid": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 disabled",
      "props": {
        "disabled": true
      },
      "source": "boolean"
    },
    {
      "label": "开启 readonly",
      "props": {
        "readonly": true
      },
      "source": "boolean"
    },
    {
      "label": "关闭 clearable",
      "props": {
        "clearable": false
      },
      "source": "boolean"
    },
    {
      "label": "rows=2",
      "props": {
        "rows": 2,
        "multiline": true
      },
      "source": "number"
    },
    {
      "label": "rows=5",
      "props": {
        "rows": 5,
        "multiline": true
      },
      "source": "number"
    }
  ],
  "ToastHost": [],
  "ActivityList": [],
  "Band": [],
  "BentoCard": [
    {
      "label": "span=hero",
      "props": {
        "span": "hero"
      },
      "source": "enum"
    },
    {
      "label": "span=side",
      "props": {
        "span": "side"
      },
      "source": "enum"
    },
    {
      "label": "span=wide",
      "props": {
        "span": "wide"
      },
      "source": "enum"
    },
    {
      "label": "span=narrow",
      "props": {
        "span": "narrow"
      },
      "source": "enum"
    },
    {
      "label": "span=half",
      "props": {
        "span": "half"
      },
      "source": "enum"
    },
    {
      "label": "span=full",
      "props": {
        "span": "full"
      },
      "source": "enum"
    }
  ],
  "BentoGrid": [],
  "KeyValueReadout": [
    {
      "label": "columns=2",
      "props": {
        "columns": 2
      },
      "source": "number"
    },
    {
      "label": "columns=4",
      "props": {
        "columns": 4
      },
      "source": "number"
    }
  ],
  "ReadoutStrip": [],
  "ShareList": [],
  "ShortcutGrid": []
}

/**
 * 组件自身声明的字面量默认值（只收可还原的字符串 / 布尔 / 数字）。
 *
 * 装配层要拿它算「基础示例真实会渲染出来的 props」：demoProps 没写的键，
 * 组件默认值就是实际值，少了这份事实源会把与默认值相同的覆盖误判成差异，
 * 派生或策展出渲染结果与基础格一致的重复示例。
 */
export const DEFAULT_PROPS: Record<string, Record<string, unknown>> = {
  "Icon": {
    "size": 18,
    "stroke": 1.6
  },
  "NeuralNet": {
    "burstKey": 0
  },
  "AskDock": {
    "placeholder": "问问系统…例如「谁能删除用户」"
  },
  "BoardView": {
    "draggable": false,
    "emptyText": "暂无"
  },
  "DeptSelect": {
    "placeholder": "请选择部门"
  },
  "DeptTree": {},
  "DictSelect": {
    "placeholder": "请选择"
  },
  "DictSwatchbook": {},
  "DictTag": {},
  "FormDialog": {
    "width": 620,
    "submitText": "保存"
  },
  "GeneratorPipeline": {},
  "InsightPanel": {},
  "ListPage": {
    "tableTitle": "数据列表",
    "rowKey": "id"
  },
  "MenuStarMap": {},
  "OrgCanvas": {},
  "PermissionButton": {
    "variant": "secondary",
    "size": "md"
  },
  "PermissionMatrix": {},
  "PermissionTrace": {},
  "PermissionTree": {},
  "PostLadder": {
    "loading": false
  },
  "SearchForm": {},
  "UserSelect": {
    "valueKey": "id",
    "placeholder": "请选择用户",
    "clearable": true
  },
  "BarChart": {
    "height": 168,
    "unit": ""
  },
  "HeatGrid": {},
  "RelationGraph": {
    "variant": "light",
    "networkAlpha": 1,
    "burstKey": 0,
    "label": "关系图",
    "pannable": false
  },
  "Swimlane": {
    "compact": false,
    "maxLanes": 8,
    "slowMs": 1000
  },
  "TickRing": {
    "unit": "%",
    "size": 168,
    "ticks": 60,
    "decimals": 1
  },
  "TrendChart": {
    "secondaryLabel": "失败",
    "primaryLabel": "数值",
    "height": 220,
    "unit": "",
    "dots": true,
    "tone": "blue"
  },
  "Affix": {},
  "Alert": {
    "type": "info",
    "showIcon": true
  },
  "Anchor": {
    "offsetTop": 0
  },
  "AutoComplete": {
    "placeholder": ""
  },
  "AvatarGroup": {
    "size": 32
  },
  "BackTop": {
    "visibilityHeight": 400,
    "right": 28,
    "bottom": 28
  },
  "Badge": {
    "max": 99,
    "tone": "danger"
  },
  "Breadcrumb": {},
  "ButtonGroup": {
    "size": "md",
    "direction": "horizontal"
  },
  "Calendar": {
    "mode": "month"
  },
  "Card": {
    "bordered": true,
    "hoverable": false,
    "loading": false
  },
  "CardGrid": {
    "columns": 3,
    "gutter": 16
  },
  "CardMeta": {
    "title": "",
    "description": "",
    "avatar": ""
  },
  "Carousel": {
    "interval": 3000,
    "loop": true,
    "indicatorPosition": "inside",
    "showArrow": "hover",
    "current": 0
  },
  "Cascader": {
    "placeholder": "请选择"
  },
  "CascaderPanel": {
    "columnWidth": 152,
    "maxHeight": 300
  },
  "CheckboxGroup": {
    "direction": "horizontal"
  },
  "Collapse": {
    "expandIconPosition": "left"
  },
  "CollapseItem": {
    "title": ""
  },
  "ColorPicker": {
    "showText": false
  },
  "Comment": {
    "author": "",
    "content": "",
    "datetime": ""
  },
  "Countdown": {
    "format": "HH:mm:ss",
    "autostart": true
  },
  "DataList": {
    "size": "md",
    "split": true
  },
  "DatePicker": {
    "placeholder": "请选择日期",
    "format": "YYYY-MM-DD"
  },
  "Descriptions": {
    "column": 3,
    "bordered": false,
    "layout": "horizontal"
  },
  "Divider": {
    "direction": "horizontal",
    "orientation": "center"
  },
  "Dropdown": {
    "trigger": "click",
    "placement": "bottom"
  },
  "DropdownButton": {
    "type": "secondary"
  },
  "DropdownSubmenu": {
    "disabled": false
  },
  "Form": {
    "layout": "vertical"
  },
  "GridCol": {
    "span": 24
  },
  "GridRow": {
    "gutter": 0,
    "justify": "start",
    "align": "stretch",
    "wrap": true
  },
  "HelpTip": {
    "tone": "info",
    "placement": "top",
    "size": 15,
    "label": "查看说明",
    "delay": 120
  },
  "Image": {
    "alt": "",
    "fit": "cover"
  },
  "ImagePreview": {
    "visible": false,
    "zoomable": true
  },
  "ImagePreviewGroup": {
    "visible": false,
    "initialIndex": 0
  },
  "InputGroup": {
    "direction": "horizontal"
  },
  "InputNumber": {
    "step": 1,
    "precision": 0
  },
  "InputPassword": {
    "modelValue": "",
    "placeholder": "请输入密码"
  },
  "InputSearch": {
    "modelValue": "",
    "placeholder": ""
  },
  "InputTag": {
    "placeholder": ""
  },
  "LinkText": {
    "target": "_self",
    "type": "primary"
  },
  "Mention": {
    "trigger": "@",
    "rows": 3
  },
  "Menu": {
    "mode": "vertical"
  },
  "MenuNode": {},
  "MonthPicker": {
    "placeholder": "请选择月份"
  },
  "Notification": {
    "type": "info",
    "showIcon": true
  },
  "OverflowList": {
    "collapseFrom": "end"
  },
  "Popconfirm": {
    "okText": "确定",
    "cancelText": "取消",
    "placement": "top"
  },
  "Popover": {
    "trigger": "hover",
    "placement": "top",
    "width": 240
  },
  "Progress": {
    "type": "line",
    "status": "normal",
    "size": 120,
    "showText": true,
    "strokeWidth": 8
  },
  "QuarterPicker": {
    "placeholder": "请选择季度"
  },
  "Radio": {},
  "RadioGroup": {
    "direction": "horizontal"
  },
  "RangePicker": {
    "placeholder": "请选择日期区间",
    "format": "YYYY-MM-DD"
  },
  "Rate": {
    "modelValue": 0,
    "count": 5
  },
  "ResizeBox": {
    "direction": "horizontal"
  },
  "Result": {
    "status": "info"
  },
  "Skeleton": {
    "loading": true,
    "animation": true,
    "rows": 1,
    "type": "text"
  },
  "Slider": {
    "modelValue": 0,
    "min": 0,
    "max": 100,
    "step": 1
  },
  "Space": {
    "direction": "horizontal",
    "size": "md",
    "align": "center",
    "wrap": false
  },
  "Spin": {
    "loading": true,
    "size": "md"
  },
  "SplitPane": {
    "direction": "horizontal"
  },
  "Steps": {
    "direction": "horizontal"
  },
  "StyledScrollbar": {
    "direction": "vertical"
  },
  "TabPane": {},
  "Tabs": {
    "type": "line"
  },
  "Textarea": {
    "modelValue": "",
    "rows": 3,
    "maxRows": 8,
    "showCount": true
  },
  "TimePicker": {
    "placeholder": "选择时间",
    "format": "HH:mm:ss"
  },
  "Timeline": {
    "mode": "left"
  },
  "TimelineItem": {
    "label": "",
    "content": "",
    "time": "",
    "dot": "default"
  },
  "Tooltip": {
    "placement": "top",
    "delay": 120
  },
  "Transfer": {},
  "Tree": {
    "checkable": false,
    "selectable": true,
    "multiple": false,
    "defaultExpandAll": false,
    "showLine": false,
    "filterText": ""
  },
  "TreeNode": {},
  "TreeSelect": {
    "placeholder": "请选择"
  },
  "Trigger": {
    "placement": "bottom",
    "popupVisible": false
  },
  "Typography": {
    "type": "text"
  },
  "Upload": {
    "limit": 0,
    "drag": false,
    "autoUpload": false
  },
  "VerificationCode": {
    "length": 6,
    "numeric": true
  },
  "Watermark": {
    "rotate": -22,
    "zIndex": 9
  },
  "WeekPicker": {
    "placeholder": "请选择周"
  },
  "YearPicker": {
    "placeholder": "请选择年份"
  },
  "AppShell": {},
  "AppearanceDialog": {},
  "CommandPalette": {},
  "PasswordDialog": {},
  "Sidebar": {},
  "Topbar": {},
  "Avatar": {
    "name": "",
    "size": 32
  },
  "Button": {
    "variant": "secondary",
    "size": "md",
    "type": "button"
  },
  "Checkbox": {},
  "ConfirmHost": {},
  "DataTable": {
    "rowKey": "id",
    "emptyText": "暂无数据",
    "expandDepth": 1
  },
  "DeltaPill": {
    "fresh": false,
    "suffix": "%"
  },
  "Drawer": {
    "width": 520
  },
  "EmptyState": {
    "title": "暂无数据",
    "icon": "search"
  },
  "Field": {},
  "HoverCard": {
    "delay": 300,
    "placement": "bottom",
    "width": 260
  },
  "IconButton": {
    "size": 17
  },
  "Metric": {
    "decimals": 0,
    "size": "m"
  },
  "Modal": {
    "width": 560
  },
  "Odometer": {
    "decimals": 0,
    "group": true
  },
  "PageHeader": {},
  "Pagination": {},
  "Panel": {},
  "Ruler": {
    "minor": 4
  },
  "SectionLabel": {},
  "Segmented": {},
  "Select": {
    "placeholder": "请选择",
    "emptyText": "无匹配项"
  },
  "SpecPlate": {},
  "StatusTag": {
    "on": "正常",
    "off": "停用"
  },
  "Switch": {},
  "Tag": {},
  "TextInput": {
    "type": "text",
    "rows": 3
  },
  "ToastHost": {},
  "ActivityList": {
    "avatarSize": 30
  },
  "Band": {
    "reveal": true
  },
  "BentoCard": {
    "span": "third",
    "glow": false
  },
  "BentoGrid": {},
  "KeyValueReadout": {
    "columns": 3
  },
  "ReadoutStrip": {},
  "ShareList": {
    "unit": ""
  },
  "ShortcutGrid": {}
}
