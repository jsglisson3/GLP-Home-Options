"""The contact form's exact wording and the lists it is built from (Checkpoint 46).

One copy. tools/build-pages.py writes the form from this file, and tools/form-test.py checks the built pages against it, so the two can never drift apart.
"""

# Joey's own text-message consent wording, copied word for word from the form he has today (the GoHighLevel form, read on Oct 26, 2026).
# DO NOT reword, trim, tidy or "fix" either sentence. "Message frequency varies." appears twice in the first one because it appears twice on his form,
# and this wording is what his text-message registration with the carriers points to. Any change is Joey's decision (research/questions-for-joey.md).
CONSENT_SERVICE = ("I consent to receive non-marketing text messages from GL Partners LLC DBA GLP Home Options regarding appointment reminders, "
                   "follow-up messages, account updates, and requested information about services. Message frequency varies. "
                   "Message frequency varies, message & data rates may apply. Reply HELP for assistance, reply STOP to opt out.")
CONSENT_MARKETING = ("I consent to receive marketing text messages from GL Partners LLC DBA GLP Home Options regarding promotions, "
                     "special offers and product updates. Message frequency varies. Message and data rates may apply. "
                     "Reply HELP for assistance, reply STOP to opt out.")

# "What can we help with?" (one tap, optional). value, label. The value is what a button's data-topic and the address's ?for= carry.
TOPICS = [
    ("sell", "Selling my home"),
    ("keep", "Keeping my home"),
    ("new", "A new home"),
    ("unsure", "Not sure yet"),
]

# "Best way to reach you" (optional, inside "Add an email, your address, or a note").
CHANNELS = [
    ("call", "Call"),
    ("text", "Text"),
    ("email", "Email"),
]

# The names the form sends, once it is connected to a place that receives them (research/form-wiring.md). "website" is the hidden trap field for robots: it is sent only when something is in it. The page never judges it (a person's password manager can fill it too, and a person must never be shown a thank-you for a request that went nowhere): the receiving end decides what to do with a request that has it, along with "seconds_on_form" (counted from when the form's script ran, which is about when the page opened).
FIELDS = ["name", "phone", "email", "topic", "topic_label", "channel", "address", "message", "consent_service", "consent_marketing", "consent_version",
          "page", "sent_at", "seconds_on_form", "website"]


def consent_version():
    """A short fingerprint of the two text-message sentences above. It goes out with every submission (consent_version), so whoever keeps the records can show
    exactly which wording a person saw when they ticked a box; it changes by itself if the wording ever does."""
    import hashlib
    return hashlib.sha1((CONSENT_SERVICE + "\n" + CONSENT_MARKETING).encode("utf-8")).hexdigest()[:8]
