# -*- coding: utf-8 -*-
from odoo import models


class SubscriptionCreditWizardReport(models.AbstractModel):
    _name = 'report.recurring_subscription.report_sub_credit'
    _description = 'Subscription Report'

    def _get_report_values(self, docids, data=None):
        wizard = self.env['credit.report.wizard'].browse(docids)

        if wizard.credit_ids and wizard.state:
            query = """
                        SELECT id
                        FROM recurring_subscription_credit
                        WHERE id = ANY(%s)
                        AND state = %s
                    """
            params = (wizard.credit_ids.ids,wizard.state)
            self.env.cr.execute(query, params)
            row = self.env.cr.fetchall()

            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription.credit'].browse(ids)
            if len(docs) == 1:
                docid = docs
            else:
                docid = None

        elif wizard.credit_ids:
            query = """
                        SELECT id
                        FROM recurring_subscription_credit
                        WHERE id = ANY(%s)
                    """

            params = (wizard.credit_ids.ids,)
            self.env.cr.execute(query, params)
            row = self.env.cr.fetchall()

            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription.credit'].browse(ids)
            if len(docs) == 1:
                docid = docs
            else:
                docid = None

        elif wizard.state:
            # domain = [
            #     ('state', 'in', wizard.state),
            # ]
            query = """
                        SELECT id
                        FROM recurring_subscription_credit
                        WHERE state = %s
                    """
            params = (wizard.state,)
            self.env.cr.execute(query, params)
            row = self.env.cr.fetchall()
            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription.credit'].browse(ids)
            if len(docs) == 1:
                docid = docs
            else:
                docid = None
            print(wizard.state)
        else:
            query = """
                        SELECT id 
                        FROM recurring_subscription_credit
                    """
            self.env.cr.execute(query)
            row = self.env.cr.fetchall()
            ids = []
            for row in row:
                ids.append(row[0])

            docs = self.env['recurring.subscription.credit'].browse(ids)
            if len(docs) == 1:
                docid = docs
            else:
                docid = None

        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription.credit',
            'docs': docs,
            'docid': docid,
            'wizard': wizard,
        }