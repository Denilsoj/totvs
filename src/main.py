from argparse import ArgumentParser

from db.config import ConfigDB
from db.queries.step_1 import UpdatedNegativeWords
from db.queries.step_2 import UpdateDispensationItems
from db.queries.step_3 import ApplyFilterByOrgan
from db.queries.step_4 import ClassifyContextWithAI
from db.queries.step_5 import SetUnclassifiedAsApproved


class Command(ArgumentParser):
    def __init__(self):
        super().__init__()

        self.add_argument("--schema", type=str, help="Schema name", required=True)
        self.add_argument("--table", type=str, help="Table name", required=True)
        self.add_argument(
            "--dump_table", type=str, help="Dump table name", required=True
        )
        self.add_argument("--ai_model", type=str, help="AI model to use", required=True)

    def run(self):
        args = self.parse_args()

        print("Running steps...")
        print(f"Schema: {args.schema}")
        print(f"Table: {args.table}")
        print(f"Dump Table: {args.dump_table}")

        print("Connecting to database...")
        config = ConfigDB()

        # print("Duplicating table and doing settings...")
        # config.duplicate_table(args.schema, args.table, args.dump_table)

        print("Running steps...")

        # print("Step 1: Negative words...")
        # step_1 = UpdatedNegativeWords(args.schema, args.table)
        # step_1.execute(config.cursor)
        # print("Step 1 done!")

        # print("Step 2: Dispensation items...")
        # step_2 = UpdateDispensationItems(args.schema, args.table)
        # step_2.execute(config.cursor)
        # print("Step 2 done!")

        # print("Step 3: Filter by organ...")
        # step_3 = ApplyFilterByOrgan(args.schema, args.table)
        # step_3.execute(config.cursor)
        # print("Step 3 done!")

        print("Step 4: Classify context with AI...")
        step_4 = ClassifyContextWithAI(args.schema, args.table, args.ai_model)
        step_4.execute(config.cursor)
        print("Step 4 done!")

        # print("Step 5: Set unclassified as approved...")
        # step_5 = SetUnclassifiedAsApproved(args.schema, args.table)
        # step_5.execute(config.cursor)
        # print("Step 5 done!")

        print("Committing changes...")
        config.connection.commit()
        print("Done!")


if __name__ == "__main__":
    cli = Command()
    cli.run()
