from datetime import timedelta
from django.db.models import F
from django.utils import timezone
from celery import shared_task
from .models import Subscription, Invoice
import logging

logger = logging.getLogger(__name__)


@shared_task
def generate_invoices():
    """Generate invoices for subscriptions that need billing today"""
    today = timezone.now().date()

    # Find active subscriptions that need billing today
    subscriptions_to_bill = Subscription.objects\
        .select_related('plan')\
        .annotate(next_billing_date=(
            F("start_date") + timedelta(days=F("plan__billing_cycle_days"))))\
        .filter(status='active', next_billing_date__date=today)

    invoices_created = 0

    for subscription in subscriptions_to_bill:
        try:
            # Check if invoice already exists for this period
            existing_invoices = Invoice.objects\
                .filter(subscription=subscription,
                        due_date__date__lt=today, paid_date__isnull=True)

            if existing_invoices.exists():
                logger.info(f"Invoice already exists for subscription {subscription.id}")  # noqa: E501
                continue

            # Create invoice
            invoice = Invoice.objects.create(
                subscription=subscription,
                user=subscription.user,
                amount=subscription.plan.price,
                due_date=timezone.now() + timedelta(days=14))

            invoices_created += 1
            logger.info(f"Created invoice {invoice.id} for subscription {subscription.id}")  # noqa: E501

        except Exception as e:
            logger.error(f"Error creating invoice for subscription {subscription.id}: {str(e)}")  # noqa: E501

    logger.info(f"Generated {invoices_created} invoices")
    return invoices_created


@shared_task
def mark_overdue_invoices():
    """Mark pending invoices as overdue if past due date"""
    overdue_invoices = Invoice.objects.filter(
        status='pending', due_date__lt=timezone.now().date())

    count = 0
    for invoice in overdue_invoices:
        invoice.status = 'overdue'
        invoice.save()
        count += 1
        logger.info(f"Marked invoice {invoice.id} as overdue")

    logger.info(f"Marked {count} invoices as overdue")
    return count


@shared_task
def send_invoice_reminders():
    """Send reminders for unpaid invoices"""
    # Find invoices that are pending or overdue
    reminder_invoices = Invoice.objects\
        .select_related("user", "subscription__plan")\
        .filter(status__in=['pending', 'overdue'])

    reminders_sent = 0

    for invoice in reminder_invoices:
        try:
            # Mock email sending (replace with actual email service)
            send_reminder_email(invoice)
            reminders_sent += 1
            logger.info(f"Sent reminder for invoice {invoice.id}")

        except Exception as e:
            logger.error(f"Error sending reminder for invoice {invoice.id}: {str(e)}")  # noqa: E501

    logger.info(f"Sent {reminders_sent} invoice reminders")
    return reminders_sent


def send_reminder_email(invoice: Invoice):
    """Mock email sending function"""
    print(f"""
    ===========================================
    INVOICE REMINDER EMAIL
    ===========================================
    To: {invoice.user.email}
    Subject: Payment Reminder - Invoice #{invoice.id}

    Dear {invoice.user.first_name or invoice.user.username},

    This is a friendly reminder that your invoice for
    {invoice.subscription.plan.name} plan is
    {'overdue' if invoice.status == 'overdue' else 'due soon'}.

    Invoice Details:
    - Amount: ${invoice.amount}
    - Due Date: {invoice.due_date.strftime('%Y-%m-%d')}
    - Status: {invoice.status}

    Please log in to your account to make the payment.

    Thank you!
    ===========================================
    """)
