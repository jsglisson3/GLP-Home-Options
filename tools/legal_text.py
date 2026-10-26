"""Wording for the legal pages (data only). tools/build-pages.py turns this into privacy-policy.html and terms-of-service.html.

The text follows the structure and promises of the policy that was on the old glphomeoptions.com site (updated February 2026),
rewritten in plain words. It has NOT been reviewed by a lawyer. See ROADMAP.md (Session 13).
"""

UPDATED = "October 21, 2026"


NOTE = (
    '<p class="doc-note"><strong>Draft for review.</strong> This page covers the same ground as the policy on the previous '
    "glphomeoptions.com site, rewritten in plain words. A real estate or privacy attorney should review it before the "
    "site goes live. <!-- REMOVE THIS NOTE AT LAUNCH --></p>"
)

PRIVACY = {
    "file": "privacy-policy.html",
    "title": "Privacy Policy",
    "meta": "How GLP Home Options collects, uses, and protects the information you share with us.",
    "lede": "How we handle the information you share with us. Last updated " + UPDATED + ".",
    "intro": "This policy explains what GLP Home Options (operated by GL Partners LLC, &ldquo;we&rdquo; or &ldquo;us&rdquo;) "
             "collects through this website, how we use it, and the choices you have. We keep it plain on purpose.",
    "sections": [
        ("1. What information we collect",
         ["<p>We collect the personal information you choose to give us when you ask about our services, for example when you "
          "fill out the contact form, book a call, call or text us, or email us. That usually means your name, email address, "
          "phone number, and details about your property.</p>"]),
        ("2. How we use your information",
         ["<p>We use what you share to communicate with you, to understand your situation, and to offer options that fit your "
          "property. We may reach out by email, phone call, or text message (SMS).</p>"]),
        ("3. How we share information",
         ["<p>We do not sell or rent your personal information to third parties.</p>",
          "<p>We may share information with trusted service providers that help us run this website and our business (for "
          "example, the software that hosts our contact form, scheduling, and messaging). They agree to keep your information "
          "confidential.</p>",
          "<p><strong>No mobile information will be shared with third parties or affiliates for marketing or promotional "
          "purposes.</strong> Text messaging originator opt-in data and consent will not be shared with any third parties.</p>"]),
        ("4. Cookies and similar technologies",
         ["<p>We use cookies and similar technologies to make browsing easier, to understand how visitors use the site, and to "
          "learn what people find helpful. Cookies are small files stored on your device that remember your preferences and "
          "recognize returning visitors.</p>",
          "<p>You can control or turn off cookies in your browser settings, though some parts of the site may not work properly "
          "without them. We respect &ldquo;Do Not Track&rdquo; signals when your browser sends them.</p>"]),
        ("5. Text messages (SMS)",
         ["<p>If you opt in, we use your phone number to text you about your inquiry. You can opt out at any time by replying "
          "<strong>STOP</strong> to any message. Message and data rates may apply.</p>"]),
        ("6. Security",
         ["<p>We use a variety of security measures to protect your personal information. No method of transmission over the "
          "Internet is 100% secure, so we cannot promise absolute security.</p>"]),
        ("7. Your rights",
         ["<p>You can ask to see the personal information we hold about you, to have it corrected, or to have it deleted. "
          "To make a request, contact us using the details below.</p>"]),
        ("8. Changes to this policy",
         ["<p>We may update this policy from time to time. When we do, we will post the new version on this page and change "
          "the date at the top.</p>"]),
        ("9. Contact us",
         ["<p>Questions or concerns about this policy? Email <a href=\"mailto:[[email]]\">[[email]]</a>. "
          "Mailing address: GLP Home Options (Legal entity: GL Partners LLC), [[address]].</p>"]),
    ],
}

TERMS = {
    "file": "terms-of-service.html",
    "title": "Terms of Service",
    "meta": "The terms for using the GLP Home Options website and receiving text messages from us.",
    "lede": "The ground rules for using this site and our text messages. Last updated " + UPDATED + ".",
    "intro": "These terms apply to your use of the GLP Home Options website. GLP Home Options is operated by GL Partners LLC "
             "(&ldquo;we&rdquo; or &ldquo;us&rdquo;).",
    "sections": [
        ("1. Agreement to these terms",
         ["<p>By accessing or using this website, you agree to these Terms of Service and to our "
          "<a href=\"privacy-policy.html\">Privacy Policy</a>. If you do not agree with any part of them, please do not use the website.</p>"]),
        ("2. For information only",
         ["<p>Everything on this website is for educational and informational purposes. It is not legal, financial, or tax advice. "
          "Please talk with a qualified professional before you make major decisions about your property.</p>",
          "<p>Figures on this site, including the side-by-side comparison and the seller net sheet, are illustrative estimates based "
          "on the numbers you enter. They are not an offer and not a guarantee of any price, cost, or timeline.</p>"]),
        ("3. Use license",
         ["<p>You may view the materials on this website for personal, non-commercial use only. This is a license to view, "
          "not a transfer of title.</p>"]),
        ("4. Limitations",
         ["<p>GLP Home Options, GL Partners LLC, and our suppliers are not liable for any damages arising from the use of, or the "
          "inability to use, the materials on this website.</p>"]),
        ("5. Revisions and errors",
         ["<p>The materials on this website may contain technical, typographical, or photographic errors. We do not promise "
          "that any of the materials are accurate, complete, or current.</p>"]),
        ("6. Text messages (SMS)",
         ["<p>When you give us your phone number, you agree to receive text messages from us about your property inquiry, "
          "appointment reminders, and follow-ups. Expect messages about your consultation request, possible offers, and answers "
          "to your questions.</p>",
          "<p>You can opt out at any time by replying <strong>STOP</strong> to any message. Message and data rates may apply.</p>"]),
        ("7. Carriers",
         ["<p>Wireless carriers are not liable for delayed or undelivered messages.</p>"]),
        ("8. Age requirement",
         ["<p>You must be at least 18 years old to use this website and our services. By using the site, you confirm that you "
          "are old enough to enter into a binding contract with GL Partners LLC.</p>"]),
        ("9. Governing law",
         ["<p>These terms are governed by the laws of the State of Tennessee. You submit to the exclusive jurisdiction of the "
          "courts located there.</p>"]),
        ("10. Questions",
         ["<p>Questions about these terms? Email <a href=\"mailto:[[email]]\">[[email]]</a>.</p>"]),
    ],
}
