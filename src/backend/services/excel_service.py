import openpyxl
from config import Config
from openpyxl.styles import Font


def add_to_excel(company, platform, job_title, url, date):
    try:
        wb = openpyxl.load_workbook(Config.EXCEL_FILE)
        ws = wb["suivi"]

        new_row_data = ["A faire", "CDI", company, platform, job_title, url, date, ""]
        ws.append(new_row_data)
        new_row_idx = ws.max_row

        for col in range(1, len(new_row_data) + 1):
            ws.cell(row=new_row_idx, column=col).font = Font(name="Roboto", size=10)

        for cell in ws[1]:
            cell.font = Font(name="Roboto", size=11)

        data = list(ws.iter_rows(min_row=2, values_only=True))
        data_sorted = sorted(data, key=lambda x: x[0] or "")

        for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
            for cell in row:
                cell.value = None

        for r_idx, row_data in enumerate(data_sorted, start=2):
            for c_idx, value in enumerate(row_data, start=1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                cell.font = Font(name="Roboto", size=11)

        wb.save(Config.EXCEL_FILE)
        wb.close()

    except Exception as e:
        print(f"Error adding to Excel: {e}")
        raise
