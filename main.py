import os
import win32com.client as win32

def fill_ks2_and_pdf(template_path, output_pdf, data):
    excel = None
    wb = None
    try:
        # 1. Запуск Excel в фоне
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        excel.ScreenUpdating = False

        wb = excel.Workbooks.Open(os.path.abspath(template_path))
        ws = wb.ActiveSheet

        # 2. Заполнение шапки
        ws.Range("E7").Value = data.get("investor", "")
        ws.Range("G9").Value = data.get("customer", "")
        ws.Range("H11").Value = data.get("contractor", "")
        ws.Range("E13").Value = data.get("construction", "")
        ws.Range("C15").Value = data.get("object", "")
        ws.Range("N24").Value = data.get("document_number", "")
        ws.Range("Q24").Value = data.get("contract_date", "")
        ws.Range("W24").Value = data.get("report_from", "")
        ws.Range("AA24").Value = data.get("report_to", "")
        ws.Range("AD6").Value = data.get("okpo_investor", "")
        ws.Range("AD8").Value = data.get("okpo_customer", "")
        ws.Range("AD10").Value = data.get("okpo_contractor", "")
        ws.Range("AD16").Value = data.get("okdp", "")
        ws.Range("AD18").Value = data.get("contract_number", "")
        ws.Range("AD19").Value = data.get("day_contract", "")
        ws.Range("AF19").Value = data.get("month_contract", "")
        ws.Range("AG19").Value = data.get("year_contract", "")
        ws.Range("O27").Value = data.get("smeta", "")

        # 3. Заполнение подписей
        ws.Range("F59").Value = data.get("surrender_position", "")
        ws.Range("N60").Value = data.get("surrender_signature", "")
        ws.Range("F64").Value = data.get("accept_position", "")
        ws.Range("N65").Value = data.get("accept_signature", "")

        # ==========================================================
        # 4. РАЗДЕЛЕНИЕ И ЗАПОЛНЕНИЕ РАБОТ (ИСПРАВЛЕНО)
        # ==========================================================
        start_row_1 = 32
        end_row_1_data = 37  # Последняя строка для данных на 1-й странице (перед "Итого")
        capacity_p1 = end_row_1_data - start_row_1 + 1  # 7 строк

        works = data.get("works", [])
        works_p1 = works[:capacity_p1]  # Работы для 1-й страницы
        works_p2 = works[capacity_p1:]  # Работы для 2-й страницы

        # Очищаем области данных от пустых строк шаблона, чтобы не было дублей
        ws.Range(f"{start_row_1}:{end_row_1_data}").ClearContents()
        ws.Range("45:53").ClearContents()  # Область данных на 2-й странице

        # Заполняем 1-ю страницу ТОЛЬКО работами, которые влезли
        row = start_row_1
        for i, work in enumerate(works_p1, start=1):
            ws.Cells(row, 1).Value = i
            ws.Cells(row, 3).Value = work.get("position", "")
            ws.Cells(row, 6).Value = work.get("name", "")
            ws.Cells(row, 15).Value = work.get("number_pricelist", "")
            ws.Cells(row, 17).Value = work.get("unit_of_measurement", "")
            ws.Cells(row, 21).Value = work.get("quantity", "")
            ws.Cells(row, 25).Value = work.get("price", "")
            ws.Cells(row, 30).Value = work.get("quantity", 0) * work.get("price", 0)
            row += 1

        # ==========================================================
        # ЛОГИКА ОБРАБОТКИ СТРАНИЦ
        # ==========================================================
        if not works_p2:
            # 📄 Сценарий 1: Все работы поместились на 1-ю страницу
            print("📄 Сценарий 1: Все работы на 1-й странице. Переносим блок итогов (4 строки).")
            
            ws.Rows("40:43").Insert()  # Вставляем место под итоги
            ws.Range("58:61").Copy()   # Копируем сдвинутый блок 54-57 -> 58-61
            ws.Range("A40").PasteSpecial(Paste=-4104)
            excel.CutCopyMode = False
            
            ws.Range("46:61").Delete() # Удаляем шапку 2-й страницы и старые дубли итогов
            
            # Удаляем пустые строки на 1-й странице перед блоком итогов
            for r in range(39, start_row_1 - 1, -1):
                if ws.Cells(r, 6).Value is None or str(ws.Cells(r, 6).Value).strip() == "":
                    ws.Rows(r).Delete()
        else:
            # 📄 Сценарий 2: Работы переносятся на 2-ю страницу
            print("📄 Сценарий 2: Работы переносятся на 2-ю страницу.")
            
            start_row_2 = 45
            row_2 = start_row_2
            start_num_2 = capacity_p1 + 1  # Сквозная нумерация (8, 9, 10...)
            
            for i, work in enumerate(works_p2, start=start_num_2):
                ws.Cells(row_2, 1).Value = i
                ws.Cells(row_2, 3).Value = work.get("position", "")
                ws.Cells(row_2, 6).Value = work.get("name", "")
                ws.Cells(row_2, 15).Value = work.get("number_pricelist", "")
                ws.Cells(row_2, 17).Value = work.get("unit_of_measurement", "")
                ws.Cells(row_2, 21).Value = work.get("quantity", "")
                ws.Cells(row_2, 25).Value = work.get("price", "")
                ws.Cells(row_2, 30).Value = work.get("quantity", 0) * work.get("price", 0)
                row_2 += 1

            # Удаляем пустые строки на 2-й странице (перед "Итого" на 54)
            for r in range(53, start_row_2 - 1, -1):
                if ws.Cells(r, 6).Value is None or str(ws.Cells(r, 6).Value).strip() == "":
                    ws.Rows(r).Delete()
            
            # Удаляем пустые строки на 1-й странице (перед "Итого" на 39)
            for r in range(38, start_row_1 - 1, -1):
                if ws.Cells(r, 6).Value is None or str(ws.Cells(r, 6).Value).strip() == "":
                    ws.Rows(r).Delete()

        # 5. Экспорт в PDF
        wb.ExportAsFixedFormat(0, os.path.abspath(output_pdf))
        print(f"✅ PDF сохранён: {output_pdf}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if wb: wb.Close(False)
        if excel: excel.Quit()
        del ws, wb, excel
        import gc
        gc.collect()


if __name__ == "__main__":
    template = r"D:\diplom_test\ks2.xls"
    output   = r"D:\diplom_test\Act_KS2_Filled.pdf"

    data = {
        "investor": "ООО «Инвестор»",
        "customer": "АО «Генподрядчик»",
        "contractor": "ООО «Подрядчик»",
        "construction": "ЖК «Солнечный»",
        "object": "Корпус 1",
        "document_number": "123-КС",
        "contract_date": "01.01.2024",
        "report_from": "01.10.2024",
        "report_to": "31.10.2024",
        "okpo_investor": "12345678",
        "okpo_customer": "87654321",
        "okpo_contractor": "11223344",
        "okdp": "4530",
        "contract_number": "N4",
        "day_contract": "04",
        "month_contract": "09",
        "year_contract": "2024",
        "smeta": "150 000 руб.",
        "surrender_position": "Главный инженер",
        "surrender_signature": "Иванов И.И.",
        "accept_position": "Руководитель проекта",
        "accept_signature": "Петров П.П.",
        "works": [
            {"position": "20-30", "name": "Устройство стяжки пола", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 150, "price": 450},
            {"position": "30-40", "name": "Штукатурка стен", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 300, "price": 320},
            {"position": "40-50", "name": "Укладка плитки", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 50, "price": 800},
            {"position": "50-60", "name": "Покраска потолков", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 120, "price": 350},
            {"position": "30-40", "name": "Штукатурка стен", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 300, "price": 320},
            {"position": "30-40", "name": "Штукатурка стен", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 300, "price": 320},
            {"position": "40-50", "name": "Укладка плитки", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 50, "price": 800},
            {"position": "50-60", "name": "Покраска потолков", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 120, "price": 350},
            {"position": "30-40", "name": "Штукатурка стен", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 300, "price": 320},
            {"position": "30-40", "name": "Штукатурка стен", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 300, "price": 320},
            {"position": "40-50", "name": "Укладка плитки", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 50, "price": 800},
            {"position": "50-60", "name": "Покраска потолков", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 120, "price": 350},
            {"position": "30-40", "name": "Штукатурка стен", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 300, "price": 320},
            {"position": "30-40", "name": "Штукатурка стен", "number_pricelist": "-", "unit_of_measurement": "м2", "quantity": 300, "price": 320},
            {"position": "90-100", "name": "Сантехнические работы", "number_pricelist": "-", "unit_of_measurement": "точка", "quantity": 15, "price": 1500} 
        ]
    }

    fill_ks2_and_pdf(template, output, data)