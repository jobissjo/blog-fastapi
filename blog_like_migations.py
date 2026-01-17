from bson import ObjectId
from app.core.db_config import db


async def migrate_likes():
    collection = db.blog_likes

    # Only fetch documents where blog_id is stored as string
    cursor = collection.find(
        {"blog_id": {"$type": "string"}},
        {"blog_id": 1}  # projection (optional but faster)
    )

    updated = 0
    skipped = 0
    print("Starting migration...")

    async for doc in cursor:
        blog_id = doc.get("blog_id")

        if not blog_id:
            skipped += 1
            continue

        if ObjectId.is_valid(blog_id):
            await collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"blog_id": ObjectId(blog_id)}}
            )
            updated += 1
        else:
            skipped += 1
            print(f"Skipped invalid blog_id: {blog_id}")

    print(f"Migration completed → Updated: {updated}, Skipped: {skipped}")


async def main():
    await migrate_likes()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
