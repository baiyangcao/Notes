<link rel="stylesheet" href="../node_modules/bootstrap/dist/css/bootstrap.css">

## `EasyUI`中`getChanges`方法获取不到`updateRow`的结果

在使用了`updateRow`更新行数据之后，使用`getChanges`方法获取表格改变，
但是却获取不到正确的结果，后在网上找到如下重写`updateRow`方法

```js
$.extend($.fn.datagrid.methods, {
    updateRow: function(jq, param) {
        return jq.each(function() {
            var target = this;
            var state = $.data(target, 'datagrid');
            var opts = state.options;
            var row = state.data.rows[param.index];
            var updated = false;
            for (var field in param.row) {
                if (row[field] != param.row[field]) {
                    updated = true;
                    break;
                }
            }
            if (updated) {
                if ($.inArray(row, state.insertedRows) == -1) {
                    if ($.inArray(row, state.updatedRows) == -1) {
                        state.updatedRows.push(row);
                    }
                }
                $.extend(row, param.row);
                opts.view.updateRow.call(opts.view, this, param.index, param.row);
            }
        });
    }
});
```

> 参考链接：<http://www.jeasyui.com/forum/index.php?topic=5372.0>