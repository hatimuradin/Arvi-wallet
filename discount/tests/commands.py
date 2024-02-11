import argparse
import sys
from pathlib import Path
from sqlmodel import create_engine, select, Session

if __name__ == "__main__" and not __package__:
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[2]

    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError:
        pass

    __package__ = "arvan-challenge.discount.tests"

from discount.models import ChargeCode

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--add", help="add number of charge codes")
parser.add_argument("--delete", action="store_true", help="delete all charge codes")

args = parser.parse_args()

engine = create_engine(
    "postgresql://discount_db_username:discount_db_password@127.0.0.1:5433/discount_db_dev",
    echo=True,
)


def main():

    try:
        if args.add is not None:
            codes = [
                ChargeCode(code="test_code", amount=10000) for _ in range(int(args.add))
            ]
            with Session(engine) as session:
                session.add_all(codes)
                session.commit()
        elif args.delete:
            query = select(ChargeCode)
            with Session(engine) as session:
                codes = session.exec(query).all()
                for c in codes:
                    session.delete(c)
                session.commit()

    except Exception as e:
        print(f"Oh come on, Give me the correct info! {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
