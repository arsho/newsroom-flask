from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
news = Table('news', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('news_title', String(length=150)),
    Column('news_body', Text),
    Column('news_author', String(length=150)),
    Column('news_date', Date),
    Column('news_user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['news'].columns['news_date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['news'].columns['news_date'].drop()
