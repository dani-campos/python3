#!/usr/bin/env python3

import json
import sys
from datetime import datetime, timedelta


class Authorizer:
    def __init__(self):
        self.line = True
        self.account = None
        self.operation = None
        self.violations = list()
        self.transaction = None
        self.transactions = list()
        self.count = 0

    def print_log(self):
        print(json.dumps(dict(
            account=self.account,
            violations=self.violations,
        )), file=sys.stdout)

    def add_violation(self, violation, log=False):
        if violation not in self.violations:
            self.violations.append(violation)
        if log:
            self.print_log()

    def get_account(self):
        if self.account:
            self.add_violation('account-already-initialized', log=True)
            return self.account
        self.account = self.operation['account']
        if 'account-already-initialized' in self.violations:
            self.violations.remove('account-already-initialized')
        if 'account-not-initialized' in self.violations:
            self.violations.remove('account-not-initialized')
        self.print_log()
        return self.account

    def _validate_limit(self):
        if self.transaction['amount'] > self.account['available-limit']:
            self.add_violation('insufficient-limit')
            self.count = 0

    def _validate_active_card(self):
        if self.account['active-card'] is not True:
            self.add_violation('card-not-active')

    def _validate_transaction_time(self):
        current_time = datetime.strptime(self.transaction['time'][:-5], '%Y-%m-%dT%H:%M:%S')
        limit_time = current_time - timedelta(minutes=2)
        if current_time >= limit_time and self.count >= 3:
            self.add_violation('high-frequency-small-interval')

    def _validate_doubled_transaction(self):
        for item in self.transactions:
            same_amount = item["amount"] == self.transaction["amount"]
            same_merchant = item["merchant"] == self.transaction["merchant"]
            if same_amount and same_merchant:
                self.add_violation('doubled-transaction')

    def _make_transaction(self):
        if not self.violations or self.violations == ['account-already-initialized']:
            if 'account-already-initialized' in self.violations:
                self.violations.remove('account-already-initialized')
            self.account['available-limit'] -= self.transaction["amount"]
            self.count += 1
        self.transactions.append(self.transaction)
        self.print_log()

    def _clear_violations(self):
        self.violations = list()

    def _make_validations_and_transaction(self):
        self._validate_active_card()
        self._validate_limit()
        self._validate_transaction_time()
        self._validate_doubled_transaction()
        self._make_transaction()
        self._clear_violations()

    def process(self):
        if 'account' in self.operation:
            self.get_account()
        if 'transaction' in self.operation.keys():
            self.transaction = self.operation['transaction']
            if not self.account:
                self.add_violation('account-not-initialized', log=True)
                return

            self._make_validations_and_transaction()

    def run(self):
        while self.line:
            self.line = sys.stdin.readline().strip()
            if not self.line:
                continue
            self.operation = json.loads(self.line)
            self.process()


if __name__ == "__main__":
    Authorizer().run()
