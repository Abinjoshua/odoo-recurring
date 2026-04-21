# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime, timedelta


class SubscriptionWizardReport(models.AbstractModel):
    _name = 'report.recurring_subscription.report_recurring_subscription'
    _description = 'Subscription Report'

    def _get_report_values(self, docids, data=None):
        wizard = self.env['subscription.report.wizard'].browse(docids)
        now = datetime.now()

        if wizard.recurring_intervals and wizard.subscription_ids:
            if wizard.recurring_intervals == 'day':
                start_date = datetime(now.year, now.month, now.day)
                end_date = start_date + timedelta(days=1)

            elif wizard.recurring_intervals == 'week':
                start_date = datetime(now.year, now.month, now.day - 7)
                end_date = start_date + timedelta(now.day)
                print(start_date)

            elif wizard.recurring_intervals == 'month':
                start_date = datetime(now.year, now.month, 1)
                if now.month == 12:
                    end_date = datetime(now.year + 1, 1, 1)
                else:
                    end_date = datetime(now.year, now.month + 1, 1)

            elif wizard.recurring_intervals == 'year':
                start_date = datetime(now.year, 1, 1)
                end_date = datetime(now.year + 1, 1, 1)

            # domain = [
            #     ('create_date', '>=', start_date),
            #     ('create_date', '<', end_date),
            #     ('id', 'in', wizard.subscription_ids),
            # ]

            query = """
                         SELECT id
                           FROM recurring_subscription
                           WHERE create_date >= %s
                           AND create_date < %s
                           AND id = ANY(%s)
                    """
            print(query)
            params = (start_date, end_date, wizard.subscription_ids.ids)
            self.env.cr.execute(query, params)
            row = self.env.cr.fetchall()
            ids = []
            for row in row:
                ids.append(row[0])
            print(ids)

            docs = self.env['recurring.subscription'].browse(ids)
            print(docs)
            if len(docs) == 1:
                docid = docs
            else:
                docid = None

        elif wizard.recurring_intervals:
            if wizard.recurring_intervals == 'day':
                start_date = datetime(now.year, now.month, now.day)
                end_date = start_date + timedelta(days=1)

            elif wizard.recurring_intervals == 'week':
                start_date = datetime(now.year, now.month, now.day - 7)
                end_date = start_date + timedelta(now.day)

            elif wizard.recurring_intervals == 'month':
                start_date = datetime(now.year, now.month, 1)
                if now.month == 12:
                    end_date = datetime(now.year + 1, 1, 1)
                else:
                    end_date = datetime(now.year, now.month + 1, 1)

            elif wizard.recurring_intervals == 'year':
                start_date = datetime(now.year, 1, 1)
                end_date = datetime(now.year + 1, 1, 1)

            query = """
                        SELECT id
                        FROM recurring_subscription
                        WHERE create_date >= %s
                        AND create_date < %s
                    """
            params = (start_date, end_date)
            self.env.cr.execute(query, params)
            row = self.env.cr.fetchall()

            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription'].browse(ids)
            if len(docs) == 1:
                docid = docs
                print(docid)
            else:
                docid = None

        elif wizard.subscription_ids:
            domain = [('id', 'in', wizard.subscription_ids)]

            docs = self.env['recurring.subscription'].search(domain)
            if len(docs) == 1:
                docid = docs
                print(docid)
            else:
                docid = None
        else:
            query = """
                        SELECT id
                        FROM recurring_subscription
                    """
            self.env.cr.execute(query)
            row = self.env.cr.fetchall()
            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription'].browse(ids)
            if len(docs) == 1:
                docid = docs
                print(docid)
            else:
                docid = None
        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription',
            'docs': docs,
            'wizard': wizard,
            'docid': docid,
        }
