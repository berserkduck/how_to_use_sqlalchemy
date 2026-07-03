"""
https://leetcode.cn/problems/customers-who-never-order/description/

Customers 表：

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
在 SQL 中，id 是该表的主键。
该表的每一行都表示客户的 ID 和名称。

Orders 表：

+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| customerId  | int  |
+-------------+------+
在 SQL 中，id 是该表的主键。
customerId 是 Customers 表中 ID 的外键( Pandas 中的连接键)。
该表的每一行都表示订单的 ID 和订购该订单的客户的 ID。



找出所有从不点任何东西的顾客。

以 任意顺序 返回结果表。

结果格式如下所示。



示例 1：

输入：
Customers table:
+----+-------+
| id | name  |
+----+-------+
| 1  | Joe   |
| 2  | Henry |
| 3  | Sam   |
| 4  | Max   |
+----+-------+
Orders table:
+----+------------+
| id | customerId |
+----+------------+
| 1  | 3          |
| 2  | 1          |
+----+------------+
输出：
+-----------+
| Customers |
+-----------+
| Henry     |
| Max       |
+-----------+

"""

from sqlalchemy import (
    String,
    select,
    text,
    ChunkedIteratorResult,
    ForeignKey,
)
from sqlalchemy.orm import Session, Mapped, mapped_column
from db import Base, engine
from utils import print_tabulate_formatted_result, insert_data_and_commit


class Customers(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customerId: Mapped[int] = mapped_column(ForeignKey("customers.id"))


Base.metadata.create_all(engine)


class Solution:
    def sql(self, session: Session) -> ChunkedIteratorResult:
        sql = """
            select
                c.name as customers
            from customers c left join orders o 
            on c.id = o.customerId
            where o.id is null 

        """
        result = session.execute(text(sql))
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        stmt = (
            select(Customers.name.label("customers"))
            .select_from(Customers)
            .outerjoin(Orders, Customers.id == Orders.customerId)
            .where(Orders.id == None)
        )
        result = session.execute(stmt)
        return result


if __name__ == "__main__":
    with Session(engine) as session:
        customers = [
            {"name": "Joe"},
            {"name": "Henry"},
            {"name": "Sam"},
            {"name": "Max"},
        ]
        orders = [{"customerId": 3}, {"customerId": 1}]

        insert_data_and_commit(customers, Customers, session)
        insert_data_and_commit(orders, Orders, session)

        print_tabulate_formatted_result(result=Solution().orm(session))
