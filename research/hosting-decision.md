# Hosting decision: where should the real site live?

**Written:** Oct 26, 2026, overnight (Checkpoint 44). **For:** Jeremy and Joey. **A decision, not a task:** nothing here has been changed. The site is still on the github.io preview and still `noindex`.
**Not legal advice.** Quotes come from the providers' own pages as they read on Oct 25, 2026 (an assistant read them through a tool that returns an extraction, so check the wording on the page before relying on it). Terms of service for the alternatives were **not** read for this draft; on Oct 26 a second reader found no commercial-use restriction in Cloudflare's two terms documents (see the table), and Netlify, Firebase and Vercel were checked only for their plan limits.

## The short version

1. **The preview is fine where it is.** Nothing about GitHub Pages is a problem for a draft nobody is meant to find.
2. **For the real business site, two things are worth a decision before launch:**
   - **GitHub's terms are unclear about a for-profit site.** They say Pages "is not intended for or allowed to be used as a free web hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions or providing commercial software as a service (SaaS)." They also say Pages is meant "primarily as a showcase for personal and organizational projects." A lead-generation site that sends people to a form somewhere else is not what the terms name (payments, software as a service), but "to run your online business" is broad and undefined. If GitHub decided it applied, I found no stated remedy: neither GitHub page says what would happen, and the Terms reserve the right to "reclaim any GitHub subdomain without liability". (The "polite email" and "we may not be able to serve your site" wording belongs to the usage-limits paragraph about size and bandwidth, not to the commercial-use sentence.) The risk is unquantified, not mild. I found no example of GitHub acting against a small-business brochure site.
   - **GitHub Pages has no setting for your own 301 redirects or response headers.** It only creates its own apex/www redirect. A GitHub community answer (undated) says "GitHub Pages does not support HTTP (e.g. 301) redirections"; no GitHub document I found lists a custom-headers setting. That does not stop the launch: the one old address that needs a redirect (`/calculator`) uses a "zero-second" refresh page, which Google says it treats as a permanent redirect, though it prefers real server redirects ("whenever possible").
3. **Moving later is cheap.** The site is plain HTML in a repository, with no build step on the server. A move is a host setup plus a DNS change, hours not days. So this is a decision about risk and tidiness, not a trap.

## The options

| Host | Cost | Real redirects and headers | What the sources showed | What to watch |
|---|---|---|---|---|
| **GitHub Pages** (today) | Free | No (a small page stands in for a redirect) | Custom domain, free certificate, automatic apex/www redirect, custom 404 page | The terms sentence above. A public repository is required on the free plan. GitHub itself recommends using `www`. |
| **Cloudflare Pages** | Free tier | Yes (a `_redirects` file, which the builder already writes in a live build; a `_headers` file would need to be added) | Limits page: 500 builds a month, 20,000 files, 25 MiB per file, 100 custom domains; no restriction on commercial use appears on that page, nor (read Oct 26 through an extraction tool) in Cloudflare's Self-Serve Subscription Agreement (Sept 12, 2025) or Developer Platform Service-Specific Terms (Sept 28, 2026) | Re-read both terms documents before signing up. My understanding (not in the research, confirm when setting up): a bare `glphomeoptions.com` address may require the domain's DNS to be managed at Cloudflare, which means copying every email record (MX, SPF, DKIM, DMARC) exactly; a `www` address can be pointed with a single record at the current DNS provider. |
| **Netlify** | Free, hard-capped | Yes | Free plan is 300 credits a month with a hard limit and no overage billing; each production deploy costs 15 credits, so a "publish on every save" habit can use up the free credits | When the credits run out, all projects are paused and visitors see a "Site not available" page (Netlify docs, updated Aug and Sept 2026). |
| **Firebase Hosting** | Free (Spark) | Yes (301 documented) | 360 MB a day of transfer, about 10 GB a month | The tightest cap of the four. |
| **Vercel** | Hobby plan is free | Yes | Hobby is "non-commercial, personal use only" | Not an option for a business without a paid plan. |

## What I would do, and what is yours to decide

- **Recommendation:** use **Cloudflare Pages** for the real site, connected to the same repository, **after** reading its terms and confirming the DNS point above. It gives real 301 redirects and headers, takes the "free hosting for your business" question off the table, and lets the repository be made private (ROADMAP D12, internal notes out of the public repository) without paying for a GitHub plan. **A second reader found no commercial-use restriction in Cloudflare's two terms documents on Oct 26, through an extraction tool, so re-read them before signing up; whether a private repository is supported on the free tier is my understanding, not something I checked.** If either turns out wrong, the next best choice is staying on GitHub Pages with the stub redirect and a calm plan to move, because the site is portable.
- **The smallest-change path:** stay on GitHub Pages at launch. Use the bare `glphomeoptions.com` address with GitHub's four A records and four AAAA records at the current DNS provider (no nameserver change, no risk to email), keep the `CNAME` file the builder writes, accept the stub redirect and the terms grey area, and revisit once the first leads are coming in.
- **Either way:** keep the DNS (the registrar login) under the family's control, not under the host, so changing hosts stays a DNS edit. Move the repository from Jeremy's personal GitHub account to an account or organisation that both Joey and Jeremy can reach, so the business is not tied to one person's login.
- **Apex or www** (decision 2 in `research/launch-checklist.md`): Google needs one consistent address. GitHub recommends `www`; the builder is set to the bare domain. Pick one, make everything match it, and create both records so the other redirects.

## Sources (read Oct 25, 2026)

- GitHub, Terms for Additional Products and Features (Pages section, effective Aug 27, 2026): https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features
- GitHub Pages limits: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- GitHub, managing a custom domain: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- Google, Redirects and Google Search (updated Apr 14, 2026): https://developers.google.com/search/docs/crawling-indexing/301-redirects
- Google, site moves with URL changes (updated Aug 20, 2026): https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- Google, site moves without URL changes (the DNS TTL advice; updated Dec 10, 2025): https://developers.google.com/search/docs/crawling-indexing/site-move-no-url-changes
- Cloudflare Pages limits (updated Sep 5, 2026): https://developers.cloudflare.com/pages/platform/limits
- Netlify, credit-based plans (Sep 5, 2025): https://www.netlify.com/changelog/netlify-pricing-update-introducing-credit-based-plans/
- Netlify docs, credit-based pricing plans (updated Sep 1, 2026): https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/
- Netlify docs, how credits work (updated Aug 12, 2026): https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/
- Cloudflare, Self-Serve Subscription Agreement (Sept 12, 2025): https://www.cloudflare.com/en-ca/terms/
- Cloudflare, Developer Platform Service-Specific Terms (Sept 28, 2026): https://www.cloudflare.com/service-specific-terms-developer-platform/
- Vercel, Hobby plan: https://vercel.com/docs/plans/hobby
- Firebase pricing: https://firebase.google.com/pricing
