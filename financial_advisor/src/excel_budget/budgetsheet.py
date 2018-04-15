import logging
from excel_budget.basicsheet import BasicSheet


class BudgetSheet(BasicSheet):
    def __init__(self, file_name):
        super(BudgetSheet, self).__init__(file_name)

    def get_daily_money_spent_list(self):
        """sum all spending data and return the value"""
        daily_total_list = []
        rows = self.get_row_data(min_row=2)
        for row in rows:
            daily_total_list.append(self._sum_row(row))
        return daily_total_list

    def get_money_spent_for_last_row(self):
        """given a string date, return the amount of money spent within a single day"""
        row = self.get_row_data(min_row=self.active_sheet.max_row, max_row=self.active_sheet.max_row)
        for r in row:
            return self._sum_row(r)

    def get_total_money_saved(self, budget):
        """given a integer budget value, return the amount of money not spent
        (saved) for each day
        """
        overall_total = 0
        daily_total_list = self.get_daily_money_spent_list()
        for total in daily_total_list:
            overall_total = overall_total + (budget - total)
        return overall_total

    def get_categories(self):
        """get the list of budgeting categories in the header
        and return it
        """
        for row in self.get_header_row_data():
            return [cell.internal_value for cell in row[1:]]

    def add_category(self, name):
        """insert a new category of <name> onto the end of the sheet"""
        self.write_to_sheet(1, self.get_next_col_index(), name)

    def write_budget_cell(self, row_title, col_title, data):
        """write a single cell of data to the excel sheet
        row_title should be a date of format YYYY-MM-DD
        col_title should be an existing category
        data should be the cell's new value
        """
        try:
            data = int(data)
        except TypeError:
            return
        row_num = self.get_row_number(row_title)
        col_num = self.get_col_number(col_title)
        if row_num == self.get_next_row_index():
            self.write_to_sheet(row_num, 1, row_title)
        self.write_to_sheet(row_num, col_num, data)

    def get_last_row_title(self):
        """returns string value of the last row's title in the form YYYY-MM-DD"""
        for row in self.get_row_data(min_row=self.active_sheet.max_row, max_row=self.active_sheet.max_row):
            cells = self._iter_cells(row)
            return cells[0].split(' ')[0]

    def get_row_number(self, row_name):
        """given the name of the row (the date), return its index"""
        row_num = 2
        for row in self.get_row_data(min_row=2):
            cells = self._iter_cells(row)
            if row_name in cells[0]:
                return row_num
            else:
                row_num += 1
        print('Adding new row for date {}'.format(row_name))
        return self.get_next_row_index()

    def get_col_number(self, col_name):
        """given the name of the column (the category), return its index"""
        col_num = 1
        headers = []
        for row in self.get_header_row_data():
            for cell in row:
                headers.append(str(cell.internal_value))
        for header in headers:
            if col_name == header:
                return col_num
            else:
                col_num += 1
        print('Adding new column for category {}'.format(col_name))
        return self.get_next_col_index()

    def _sum_row(self, row):
        total = 0
        cells = self._iter_cells(row)
        for cell in cells:
            try:
                total = total + float(cell)
            except Exception:
                pass
        return total
