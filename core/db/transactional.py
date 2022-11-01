from enum import Enum
from functools import wraps

from core.db import session


class Transactional:
    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            try:
                results = await function(*args, **kwargs)
                meta_result = await session.commit()
                if results:
                  if type(results) == list:
                    for result in results:
                      await session.refresh(result)
                  else:
                     await session.refresh(results)
            except Exception as e:
                await session.rollback()
                raise e

            return results, meta_result

        return decorator
