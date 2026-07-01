from typing import Type
from sqlalchemy.orm import DeclarativeBase, Session

def insert_data_and_commit(data_list: list[dict], model: Type[DeclarativeBase], session: Session) -> None:
    """
    插入数据并提交事务

    args:
        data_list: 数据列表
        model: 模型类
        session: 会话对象
    """
    for i in range(len(data_list)):
        instance = model(**data_list[i])
        session.add(instance)
    
    session.commit()
