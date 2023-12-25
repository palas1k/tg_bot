import asyncio

from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.future import select
import sqlalchemy.exc


Base = declarative_base()


class AsyncDatabaseSession:
    name_admin_db: str = "postgres"  # Имя админа
    password_db: str = "Vfnhtif1"  # Пароль бд
    ip_db: str = "localhost"  # IP бд
    name_db: str = "bottg"  # Имя бд
    connect_db: str = f"{name_admin_db}:{password_db}@{ip_db}/{name_db}"

    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def init(self):
        self._engine = create_async_engine(f"postgresql+asyncpg://{self.connect_db}", echo=True)
        self._session = async_sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


async_db_session = AsyncDatabaseSession()


class MethodClassAll:
    @classmethod
    async def update(cls, id_l: int, **kwargs):
        query = (
            sqlalchemy.sql.update(cls)
            .where(cls.id == id_l)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get_all(cls):
        query = select(cls)
        results = await async_db_session.execute(query)
        return results.all()

    @classmethod
    async def create(cls, acc) -> None:
        async_db_session.add(acc)
        await async_db_session.commit()


class MethodClassUser(MethodClassAll):
    @classmethod
    async def get_user(cls, first_name: str, all_l: bool = False):
        query = select(cls).where(cls.first_name == first_name)
        result = await async_db_session.execute(query)
        if not all_l:
            try:
                (result,) = result.one()
            except sqlalchemy.exc.NoResultFound:
                result = None
            return result
        else:
            return result.fetchall()


class MethodClassList(MethodClassAll):
    @classmethod
    async def get_list(cls, url: str):
        query = select(cls).where(cls.url == url)
        result = await async_db_session.execute(query)
        try:
            (result,) = result.one()
        except sqlalchemy.exc.NoResultFound:
            result = None
        return result


class MethodClassReporting(MethodClassAll):
    @classmethod
    async def get_report(cls, url: str):
        query = select(cls).where(cls.url == url)
        result = await async_db_session.execute(query)
        try:
            (result,) = result.one()
        except sqlalchemy.exc.NoResultFound:
            result = None
        return result

    @classmethod
    async def get_reporting_status_false(cls):
        query = select(cls).filter(cls.state == "Waiting")
        result = await async_db_session.execute(query)
        return [i[0] for i in result.all()]


class User(Base, MethodClassUser):
    __tablename__ = "user"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    id_tg = Column(BigInteger)
    ban = Column(String)
    id_reporting: Mapped[list["Reporting"]] = relationship()

    def __init__(self, first_name: str, id_tg: int, ban: str, last_name: str = None):
        self.first_name = first_name
        self.id_tg = id_tg
        self.last_name = last_name
        self.ban = ban


class Reporting(Base, MethodClassReporting):
    __tablename__ = "reporting"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    url = Column(String)
    state = Column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    def __init__(self, url: str, user_id: int, state: str):
        self.url = url
        self.user_id = user_id
        self.state = state


class WhiteList(Base, MethodClassList):
    __tablename__ = "whitelist"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String)
    url = Column(String)

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url


async def main():
    await async_db_session.init()
    await async_db_session.create_all()

if __name__ == '__main__':
    asyncio.run(main())
