# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, math, json
import erpnext
from frappe import _
from frappe.utils import flt, rounded, add_months,add_days, nowdate, getdate
from erpnext.controllers.accounts_controller import AccountsController
from erpnext.payroll.doctype.loan.loan import Loan

@frappe.whitelist()
def overwrite_validate(self,method):
	validate_repayment_method(self.repayment_method, self.loan_amount, self.monthly_repayment_amount, self.repayment_periods)
	self.set_missing_fields()
	custom_make_repayment_schedule(self)
	self.set_repayment_period()
	self.calculate_totals()
	self.set_status(from_validate=True)


@frappe.whitelist()
def custom_make_repayment_schedule(self):
	self.repayment_schedule = []
	payment_date = self.repayment_start_date
	balance_amount = self.loan_amount
	while(balance_amount > 0):
		if self.payment_in == "Monthly":
			interest_amount = rounded(balance_amount * flt(self.rate_of_interest) / (12*100))
		else:
			interest_amount = rounded(balance_amount * flt(self.rate_of_interest) / (4*12*100))
		
		principal_amount = self.monthly_repayment_amount - interest_amount
		balance_amount = rounded(balance_amount + interest_amount - self.monthly_repayment_amount)

		if balance_amount < 0:
			principal_amount += balance_amount
			balance_amount = 0.0

		total_payment = principal_amount + interest_amount
		self.append("repayment_schedule", {
			"payment_date": payment_date,
			"principal_amount": principal_amount,
			"interest_amount": interest_amount,
			"total_payment": total_payment,
			"balance_loan_amount": balance_amount
		})
		if self.payment_in == "Monthly":
			next_payment_date = add_months(payment_date, 1)
		else:
			next_payment_date = add_days(payment_date, 7)
		#untuk menambah payment 7 hari 
		
		payment_date = next_payment_date

def validate_repayment_method(repayment_method, loan_amount, monthly_repayment_amount, repayment_periods):
	if repayment_method == "Repay Over Number of Periods" and not repayment_periods:
		frappe.throw(_("Please enter Repayment Periods"))

	if repayment_method == "Repay Fixed Amount per Period":
		if not monthly_repayment_amount:
			frappe.throw(_("Please enter repayment Amount"))
		if monthly_repayment_amount > loan_amount:
			frappe.throw(_("Monthly Repayment Amount cannot be greater than Loan Amount"))
