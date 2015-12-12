import unittest
from malalaoshi.Question1.Solution import Employee


class MyTestCase(unittest.TestCase):
    id2name = {}
    emp_list = []

    write = print

    def makeReport(self, emp: Employee, reports: [Employee]):
        for one_report in reports:
            emp.addReports(one_report)

    def makeEmployee(self, emp_id: int, emp_name: str) -> Employee:
        self.id2name[emp_id] = emp_name
        return Employee(emp_id, emp_name)

    def setUp(self):
        self.id2name = {}
        self.Bill = self.makeEmployee(0, "Bill")
        self.Dom = self.makeEmployee(1, "Dom")
        self.Samir = self.makeEmployee(2, "Samir")
        self.Michael = self.makeEmployee(3, "Michael")
        self.Bob = self.makeEmployee(4, "Bob")
        self.Peter = self.makeEmployee(5, "Peter")
        self.Porter = self.makeEmployee(6, "Porter")
        self.Milton = self.makeEmployee(7, "Milton")
        self.Nina = self.makeEmployee(8, "Nina")
        self.makeReport(self.Bill, [self.Dom, self.Samir, self.Michael])
        self.makeReport(self.Dom, [self.Peter, self.Bob, self.Porter])
        self.makeReport(self.Peter, [self.Milton, self.Nina])

    def tearDown(self):
        pass

    # 测试能否正确生成Reports
    def testReports(self):
        self.write(self.Bill.getReports())
        self.assertEqual([self.Dom, self.Samir, self.Michael], self.Bill.getReports())
        self.assertNotEqual([self.Dom, self.Samir], self.Bill.getReports())

    # 测试全部路径是否正确
    def test_full_path(self):
        all_path = self.Bill._getAllPath([])
        self.print_full_path(all_path)
        self.write(all_path)
        expect_data = {
            0: [self.Bill],
            1: [self.Bill, self.Dom],
            2: [self.Bill, self.Samir],
            3: [self.Bill, self.Michael],
            4: [self.Bill, self.Dom, self.Bob],
            5: [self.Bill, self.Dom, self.Peter],
            6: [self.Bill, self.Dom, self.Porter],
            7: [self.Bill, self.Dom, self.Peter, self.Milton],
            8: [self.Bill, self.Dom, self.Peter, self.Nina]}
        self.assertEqual(expect_data, all_path)
        expect_data.pop(8)
        self.assertNotEqual(expect_data, all_path)

    # 辅助函数,化简问题中的our_boss,让它更直观
    def our_boss(self, first, second) -> Employee:
        ceo = self.Bill
        boss = Employee.closetCommonManager(ceo, first, second)
        self.write("{first} and {second}'s boss is {boss}".format(
                first=first, second=second, boss=boss))
        return boss

    # 测试问题
    def test_sample(self):
        self.assertEqual(self.Peter, self.our_boss(self.Milton, self.Nina))
        self.assertEqual(self.Dom, self.our_boss(self.Nina, self.Porter))
        self.assertEqual(self.Bill, self.our_boss(self.Nina, self.Samir))
        self.assertEqual(self.Peter, self.our_boss(self.Peter, self.Nina))

    # 将id转换为名字,方便调试
    def print_full_path(self, full_path: dict):
        for key, val in full_path.items():
            self.write("{name}: {list}".format(name=self.id2name[key],
                                               list="->".join(map(lambda item: item.emp_name, val))))

    def test_none(self):
        """
        很特殊的情况,测试两个雇员没有共同的boss
        :return: None
        """
        try:
            Employee.closetCommonManager(self.Dom, self.Milton, self.Michael)
        except ValueError as e:
            self.assertEqual(str(e), "secondEmployee not in ceo's manage scope")

    def test_same(self):
        """
        特殊情况,两个是同一个雇员
        :return: None
        """
        try:
            Employee.closetCommonManager(self.Bill, self.Milton, self.Milton)
        except ValueError as e:
            self.assertEqual(str(e), "first and second employee are same.")

    def test_ceo_and_employee_are_same(self):
        """
        特殊情况,当ceo也是比较的雇员时
        :return:
        """
        self.assertEqual(Employee.closetCommonManager(self.Bill, self.Bill, self.Milton), self.Bill)

    def test_ceo_are_employee_and_another_is_not_in_manage_scopt(self):
        """
        ceo是比较的雇员,但某个雇员不在管辖范围
        :return:
        """
        try:
            Employee.closetCommonManager(self.Dom, self.Dom, self.Michael)
        except ValueError as e:
            self.assertEqual(str(e), "secondEmployee not in ceo's manage scope")

if __name__ == '__main__':
    unittest.main()
