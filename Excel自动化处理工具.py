import os
import pandas as pd
from datetime import datetime

def merge_excel_files(input_folder, output_file):
    """合并指定文件夹下的所有 Excel 文件到一个新文件"""
    all_data = []
    file_stats = []  # 记录每个文件的统计信息

    # 遍历文件夹下的所有 Excel 文件
    for filename in os.listdir(input_folder):
        if filename.endswith(('.xlsx', '.xls')):
            file_path = os.path.join(input_folder, filename)
            try:
                # 读取 Excel 文件的所有 sheet
                xls = pd.ExcelFile(file_path)
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    df['source_file'] = filename  # 添加来源文件名标记
                    df['source_sheet'] = sheet_name  # 添加来源 sheet 标记
                    all_data.append(df)
                # 记录文件统计信息
                file_stats.append({
                    'filename': filename,
                    'sheets': len(xls.sheet_names),
                    'total_rows': sum(len(pd.read_excel(xls, sheet_name=sheet)) for sheet_name in xls.sheet_names)
                })
                print(f"成功处理文件: {filename}")
            except Exception as e:
                print(f"处理文件 {filename} 失败: {e}")

    if not all_data:
        print("未找到可处理的 Excel 文件！")
        return

    # 合并所有数据并保存
    merged_df = pd.concat(all_data, ignore_index=True)
    merged_df.to_excel(output_file, index=False)
    print(f"合并完成！结果已保存至: {output_file}")

    # 生成统计信息并保存
    stats_df = pd.DataFrame(file_stats)
    stats_file = output_file.replace('.xlsx', '_stats.xlsx')
    stats_df.to_excel(stats_file, index=False)
    print(f"数据统计已保存至: {stats_file}")

if __name__ == "__main__":
    # 输入文件夹（示例文件夹，可修改为实际路径）
    input_folder = "example"
    # 输出文件名（带时间戳，避免覆盖）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"merged_result_{timestamp}.xlsx"
    # 执行合并
    merge_excel_files(input_folder, output_file)