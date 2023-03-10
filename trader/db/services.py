from typing import List, Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import AssetCreate, AssetUpdate, AssetSchema, TradeCreate, TradeUpdate, TradeSchema
from .models import Asset, Trade


async def create_asset(db: AsyncSession, asset: AssetCreate) -> AssetSchema:
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    await db.commit()
    await db.refresh(db_asset)
    return AssetSchema.from_orm(db_asset)


async def get_asset(db: AsyncSession, asset_id: int) -> Optional[Asset]:
    db_asset = await db.get(Asset, asset_id)
    return AssetSchema.from_orm(db_asset) if db_asset else None


async def get_assets(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[AssetSchema]:
    query = await db.execute(Asset.select().offset(skip).limit(limit))
    db_assets = query.scalars().all()
    return [AssetSchema.from_orm(db_asset) for db_asset in db_assets]


async def update_asset(db: AsyncSession, asset_id: int, asset: AssetUpdate) -> Type[Asset] | None:
    db_asset = await db.get(Asset, asset_id)
    for field, value in asset:
        setattr(db_asset, field, value)
    await db.commit()
    await db.refresh(db_asset)
    return db_asset


async def delete_asset(db: AsyncSession, asset_id: int) -> None:
    await db.delete(await db.get(Asset, asset_id))
    await db.commit()


async def create_trade(db: AsyncSession, trade: TradeCreate) -> Trade:
    db_trade = Trade(**trade.dict())
    db.add(db_trade)
    await db.commit()
    await db.refresh(db_trade)
    return db_trade


async def get_trade(db: AsyncSession, trade_id: int) -> Optional[TradeSchema]:
    db_trade = await db.get(Trade, trade_id)
    return TradeSchema.from_orm(db_trade) if db_trade else None


async def get_trades(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Trade]:
    return await db.query(Trade).offset(skip).limit(limit).all()


async def update_trade(db: AsyncSession, trade_id: int, trade: TradeUpdate) -> Type[Trade] | None:
    db_trade = await db.get(Trade, trade_id)
    for field, value in trade:
        setattr(db_trade, field, value)
    await db.commit()
    await db.refresh(db_trade)
    return db_trade


async def delete_trade(db: AsyncSession, trade_id: int) -> None:
    await db.delete(await db.get(Trade, trade_id))
    await db.commit()
