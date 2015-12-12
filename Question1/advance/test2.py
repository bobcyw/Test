import unittest
from malalaoshi.Question1.advance.Solution2 import Employee, closet_common_manager, closet_common_manager2
from datetime import datetime


class MyTestCase(unittest.TestCase):
    id2name = {}
    emp_list = []

    write = print

    def make_report(self, emp: Employee, reports: [Employee]):
        for one_report in reports:
            emp.add_reports(one_report)

    def make_employee(self, emp_id: int, emp_name: str) -> Employee:
        self.id2name[emp_id] = emp_name
        return Employee(emp_id, emp_name)

    def setUp(self):
        self.id2name = {}
        self.Bill = self.make_employee(0, "Bill")
        self.Dom = self.make_employee(1, "Dom")
        self.Samir = self.make_employee(2, "Samir")
        self.Michael = self.make_employee(3, "Michael")
        self.Bob = self.make_employee(4, "Bob")
        self.Peter = self.make_employee(5, "Peter")
        self.Porter = self.make_employee(6, "Porter")
        self.Milton = self.make_employee(7, "Milton")
        self.Nina = self.make_employee(8, "Nina")
        self.make_report(self.Bill, [self.Dom, self.Samir, self.Michael])
        self.make_report(self.Dom, [self.Peter, self.Bob, self.Porter])
        self.make_report(self.Peter, [self.Milton, self.Nina])

    def tearDown(self):
        pass

    # 测试能否正确生成Reports
    def test_reports(self):
        self.write(self.Bill.reports)
        self.assertEqual([self.Dom, self.Samir, self.Michael], self.Bill.reports)
        self.assertNotEqual([self.Dom, self.Samir], self.Bill.reports)

    # 测试全部路径是否正确
    def test_full_path(self):
        all_path = self.Bill.get_all_path()
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
        boss = closet_common_manager(ceo, first, second)
        # self.write("{first} and {second}'s boss is {boss}".format(
        #         first=first, second=second, boss=boss))
        return boss

    # 测试问题
    def test_sample(self):
        start = datetime.now()
        loop_times = 10000
        for i in range(loop_times):
            self.assertEqual(self.Peter, self.our_boss(self.Milton, self.Nina))
            self.assertEqual(self.Dom, self.our_boss(self.Nina, self.Porter))
            self.assertEqual(self.Bill, self.our_boss(self.Nina, self.Samir))
            self.assertEqual(self.Peter, self.our_boss(self.Peter, self.Nina))
        end = datetime.now()
        cost_time = end-start
        self.write("test_sample run {loop_times} time cost time is {cost_time} ms".format(
                cost_time=cost_time.microseconds/1000, loop_times=loop_times))

    # 辅助函数,化简问题中的our_boss,让它更直观
    def our_boss2(self, full_path, first, second) -> Employee:
        boss = closet_common_manager2(full_path, first, second)
        # self.write("{first} and {second}'s boss is {boss}".format(
        #         first=first, second=second, boss=boss))
        return boss

    # 测试问题,动态优化版
    def test_sample2(self):
        start = datetime.now()
        loop_times = 10000
        full_path = self.Bill.get_all_path()

        for i in range(loop_times):
            self.assertEqual(self.Peter, self.our_boss2(full_path, self.Milton, self.Nina))
            self.assertEqual(self.Dom, self.our_boss2(full_path, self.Nina, self.Porter))
            self.assertEqual(self.Bill, self.our_boss2(full_path, self.Nina, self.Samir))
            self.assertEqual(self.Peter, self.our_boss2(full_path, self.Peter, self.Nina))

        end = datetime.now()
        cost_time = end-start
        self.write("test_sample2 run {loop_times} time cost time is {cost_time} ms".format(
                cost_time=cost_time.microseconds/1000, loop_times=loop_times))

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
            closet_common_manager(self.Dom, self.Milton, self.Michael)
        except ValueError as e:
            self.assertEqual(str(e), "second_employee not in ceo's manage scope")
        try:
            all_path = self.Dom.get_all_path()
            closet_common_manager2(all_path, self.Milton, self.Michael)
        except ValueError as e:
            self.assertEqual(str(e), "second_employee not in ceo's manage scope")

    def test_same(self):
        """
        特殊情况,两个是同一个雇员
        :return: None
        """
        try:
            closet_common_manager(self.Bill, self.Milton, self.Milton)
        except ValueError as e:
            self.assertEqual(str(e), "first and second employee are same.")
        try:
            all_path = self.Bill.get_all_path()
            closet_common_manager2(all_path, self.Milton, self.Milton)
        except ValueError as e:
            self.assertEqual(str(e), "first and second employee are same.")

    def test_ceo_and_employee_are_same(self):
        """
        特殊情况,当ceo也是比较的雇员时
        :return:
        """
        self.assertEqual(closet_common_manager(self.Bill, self.Bill, self.Milton), self.Bill)
        all_path = self.Bill.get_all_path()
        self.assertEqual(closet_common_manager2(all_path, self.Bill, self.Milton), self.Bill)

    def test_ceo_are_employee_and_another_is_not_in_manage_scopt(self):
        """
        ceo是比较的雇员,但某个雇员不在管辖范围
        :return:
        """
        try:
            closet_common_manager(self.Dom, self.Dom, self.Michael)
        except ValueError as e:
            self.assertEqual(str(e), "second_employee not in ceo's manage scope")
        try:
            all_path = self.Dom.get_all_path()
            closet_common_manager2(all_path, self.Dom, self.Michael)
        except ValueError as e:
            self.assertEqual(str(e), "second_employee not in ceo's manage scope")


if __name__ == '__main__':
    unittest.main()
