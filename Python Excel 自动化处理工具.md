# Python Excel 自动化处理工具

批量合并多个 Excel 文件的数据，并生成统计信息，适用于办公数据整合场景。

## 功能
- 自动读取指定文件夹下的所有 Excel 文件（支持 .xlsx/.xls）
- 合并所有 sheet 数据到新文件，并标记来源文件和 sheet 名
- 生成数据统计（文件名、sheet 数量、总行数）

## 使用方法
1. 安装依赖：`pip install -r requirements.txt`
2. 将待处理的 Excel 文件放入 `example` 文件夹（或修改 `input_folder` 路径）
3. 运行脚本：`python excel_processor.py`
4. 结果文件（合并数据 + 统计信息）会自动生成到根目录

## 示例
- 输入：`example/data1.xlsx`（3 个 sheet，共 100 行）、`example/data2.xlsx`（2 个 sheet，共 50 行）
- 输出：`merged_result_20231101_120000.xlsx`（合并后 150 行 + 来源标记）、`merged_result_20231101_120000_stats.txt`（统计信息）
