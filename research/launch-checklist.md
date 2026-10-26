# Launch checklist: from the preview site to a site Google can find

**Written:** Oct 25–26, 2026, overnight (Checkpoint 44). **For:** Jeremy first, then Joey.
**Status: DRAFT. Nothing in this file has been done.** The site is still `noindex` and lives only on the github.io preview address. Nothing here happens until Jeremy and Joey say go.
**Not legal advice.** Anything about rules is a question for a Tennessee attorney; the sources are listed in `research/hosting-decision.md` and the private research report.

## The switch, in one paragraph

The page builder (`tools/build-pages.py`) has one line near the top, `LIVE = False`.

- **`LIVE = False` (today, the preview).** The address is `https://jsglisson3.github.io/GLP-Home-Options/`. Every page says `noindex, nofollow`. There is no canonical tag, no `sitemap.xml`, no `robots.txt`, no `CNAME`.
- **`LIVE = True` (launch).** The address is `https://glphomeoptions.com`. `noindex` is gone from every page except the "page not found" page. Every page names its own address (canonical, without `.html`, because the old site's addresses had no `.html`). The builder also writes `sitemap.xml`, `robots.txt` (everything allowed, plus the sitemap line; it never blocks anything), `CNAME` (for GitHub Pages), `_redirects` (for Cloudflare Pages or Netlify) and a small `calculator.html` so the old `/calculator` link lands on the net sheet.
- **How it was tested.** `python3 tools/seo-check.py` builds both versions in a scratch folder and checks them against each other without touching the saved pages (570 checks; it currently reports `FAILS 0`). An independent reviewer then tried 43 deliberate breakages of the builder, such as a second `noindex` tag, a canonical outside the head, structured data removed, a wrong address, the preview address left in a launch file or a catch-all redirect. The check stops 39 of them (the builder itself refuses one more); the other four are not mistakes it can judge: a typo in the domain, the `www.` choice (decision 2), and two address edits that are consistent by design. **Look at the `REAL is https…` line it prints and read the domain by eye.** `python3 tools/seo-check.py --launch` adds the checks that are open on purpose today (see A1).

**The rule that matters most:** do not flip the switch on its own. The moment a live build is committed and pushed, GitHub publishes it. If the domain still shows the old GoHighLevel site, the new pages would be indexable but would point at addresses that do not exist yet. Flip it **in the same release as the domain change** (step C below), never before.

## 0. What must be decided first (nothing below can start without these)

| # | Decision | Who | Why it gates launch |
|---|---|---|---|
| 1 | **Where the site is hosted:** stay on GitHub Pages, or move to Cloudflare Pages (free) | Jeremy and Joey | GitHub's terms say Pages is "not intended for or allowed to be used as a free web hosting service to run your online business"; it also has no setting for your own 301 redirects. See `research/hosting-decision.md`. |
| 2 | **Apex or www:** `glphomeoptions.com` (what the builder uses) or `www.glphomeoptions.com` | Jeremy and Joey | One host only; every canonical, sitemap line, Google listing link and structured-data address must match it. To use www, change `REAL` in the builder. |
| 3 | **The public address and the Google listing:** show the Hixson address, or hide it and list a service area (Google does not accept a PO box as the business address) | Joey | Decides what the site, the listing and every directory say. The site's footer, Contact page and structured data currently say `PO Box 55, Hixson, TN`. |
| 4 | **The one main phone number** | Joey | Site, Google listing, Facebook and directories must show the same number. The site uses (423) 451-5707. |
| 5 | **Who holds the registrar and DNS logins**, and the GoHighLevel and GitHub accounts | Joey | Every DNS step below needs them. Keep the logins with the family, not with a host. |
| 6 | **Photos confirmed or replaced** (ROADMAP D9) | Joey | The site presents the people photos as real moments. |
| 7 | **The two legal pages read by a Tennessee attorney**, and the "Draft for review" notes removed | Joey | `tools/legal_text.py` still carries a visible draft note and the comment `REMOVE THIS NOTE AT LAUNCH`. |
| 8 | **Internal notes out of the public repository** (ROADMAP D12) | Jeremy | The repository is public. Moving the site to Cloudflare Pages lets the repository be private for free. |
| 9 | **Joey's texting and consent wording settled**, and the form tested end to end | Joey, with an attorney | The form lives inside GoHighLevel and is not changed by this switch. |

## A. Before anything else: prepare (no risk, can be done in advance)

1. Run `python3 tools/checkpoint.py` and `python3 tools/seo-check.py --launch`. Both must say clean / `FAILS 0` on the commit you plan to launch from. (Until the two legal pages have been read by an attorney and the visible "Draft for review" note is removed, `--launch` says `FAILS 2`, one per legal page. That is the right answer: decision 7 is still open.)
2. Look at the live build without publishing it: `GLP_BUILD=live python3 tools/build-pages.py` writes the live pages into your working folder, so run it in a **copy** of the project, not the real folder. (`tools/seo-check.py` does this for you in a scratch folder and tests it; use that for the check and only flip the real switch on launch day.)
3. **Write down the old site's addresses.** The old GoHighLevel site served `/` , `/about`, `/options`, `/calculator`, `/contact`, `/terms-of-service` and `/privacy-policy`. The new site uses the same names, so only `/calculator` needs a redirect (already built). Check whether `/home` also exists on the old site; if it does, add `"home": "/"` to `REDIRECTS` in the builder. Then list everything Google already knows: Search Console (Performance → Pages, and the Page indexing report) once it is verified, plus `site:glphomeoptions.com` in Google.
4. **Write down every DNS record on the domain** (a screenshot of the registrar's DNS page is enough): especially MX, SPF, DKIM and DMARC records, which carry `info@glphomeoptions.com` and GoHighLevel's email, and any GoHighLevel records. **Only the web records change** (the apex A/AAAA records and the `www` record). Never delete an email record.
5. Make sure the GoHighLevel form still loads and sends from the new pages (it is an iframe from `links.voiseai.com`, so it should not care where the domain points, but test it from a non-production page first). Send yourself one test lead. Do not send anything to a real customer.

## B. One to two weeks before launch day

1. **Verify the domain in Google Search Console** as a *Domain* property, using the DNS TXT record method, **on the old live site**. This works before any move and starts collecting data. Also add the site to Bing Webmaster Tools.
2. **Lower the DNS TTL** on the web records to a few hours, at least a week before the move (Google's guidance for site moves without URL changes). It makes the way back fast.
3. Export a baseline from Search Console (top pages and queries) and note where the site ranks today for "GLP Home Options" and a few searches that matter, so there is something to compare with.
4. Create the Google Business Profile **only after** decision 3 (address). Use the same name, phone, address (or service area) and website address the site will use. Use the final launch address as the website link, not an address that redirects.
5. Confirm no firewall or security setting on the new host blocks Googlebot.

## C. Launch day (low-traffic window, family available; the order matters)

1. **Host side first.** On GitHub Pages: add the custom domain under Settings → Pages *before* touching DNS. GitHub then adds a commit with a `CNAME` file to the branch, so pull it before your next push, and do not push a preview build between this step and step 4 (a preview build deletes `CNAME`). On Cloudflare Pages: connect the repository and add the custom domain.
2. **DNS next.** Change only the web records: the apex A and AAAA records (GitHub lists four of each) or the host's records, and the `www` record. Remove leftover web records pointing at the old host if they block the certificate. Leave MX, SPF, DKIM and DMARC alone.
3. Wait for the DNS check and the security certificate, then turn on **Enforce HTTPS** (GitHub says it can take up to 24 hours).
4. **Flip the switch in the same release:** set `LIVE = True` in `tools/build-pages.py`, run `python3 tools/build-pages.py`, run `python3 tools/seo-check.py --launch` and `python3 tools/check-links.py`, then commit and push. The pages, `sitemap.xml`, `robots.txt`, `CNAME` and the redirect files go out together. Do **not** remove `noindex` while the site is reachable only on github.io.
5. Open the live site and walk through: Home, each page, the 404 (a made-up address must show "Page not found"), `/calculator` (must reach the net sheet), the form, a text-tap and a call-tap on a real phone, and `https://glphomeoptions.com/robots.txt` and `/sitemap.xml`.

## D. After launch

**Day 0 to 2**
- In Search Console: submit `sitemap.xml`; use URL Inspection on the home page and the two or three most important pages and click Request indexing.
- Check the page source of the live home page for `noindex` (there must be none), the canonical (must be the real domain) and the JSON-LD (Google's Rich Results Test should show Local business with no errors. FAQ is no longer a Google rich result and site-name (WebSite) markup is not shown in that tool, so check those two in the page source or with a general schema validator).
- Run PageSpeed Insights on the live Home and Options pages.
- Update the Google Business Profile website link (with a UTM tag), Facebook, and any directory listings to the final address.
- If the custom form styling (`research/ghl-form-custom.css`) was pasted into GoHighLevel, change the font address on its line 4 from the preview address to the real domain (`research/ghl-form-style.md` says where).
- Visit the old preview address (`jsglisson3.github.io/GLP-Home-Options/`) once. If the site stays on GitHub Pages with the custom domain it should land on the real domain; I could not confirm that from GitHub's own pages. If hosting moved to Cloudflare Pages and GitHub Pages was left on, the old address would likely keep serving a copy of the launch build (its "page not found" page would likely look unstyled, because it links its styles from the site root), so turn GitHub Pages off once the move is stable. Both points are inferred, not tested.
- Send one more test lead end to end.

**Weeks 1 to 4**
- Watch Search Console → Page indexing for "noindex", "blocked by robots.txt", "soft 404" or "page with redirect" exclusions, and the crawl and 404 reports. Expect a temporary wobble in rankings for a few weeks (Google says "a few weeks for most pages to move").
- Keep the DNS TTL low until things are stable, then raise it.
- Optional tidy-up, not needed for launch: the pages link to Home as `index.html` (and `index.html#faq`, `index.html#how`, `index.html#numbers`) while Home's canonical is `/`. Google treats the two as one page because of the canonical, so nothing breaks; a later change to the live build could write `./` instead so the site names Home one way everywhere. Changing it changes every page's links, so do it as its own checkpoint with `tools/check-links.py` and `tools/seo-check.py`.

**Months 1 to 12 and beyond**
- Keep the `/calculator` redirect (and any other old-address redirect) for at least a year; Google's guidance is "generally at least 1 year".
- Keep the DNS TXT record that verifies Search Console.
- After every change to the builder, run `python3 tools/seo-check.py` again (canonical, sitemap and redirects can drift).
- Do not shut down or repoint the old GoHighLevel site pages until traffic to them has stopped.

## E. The way back

- **First choice: fix forward.** Most problems (a wrong word, a broken link, a missing redirect) are fixed by editing, rebuilding and pushing. Do not flip back to `noindex` just because something small is wrong: once Google has indexed pages, `noindex` removes them from results.
- **If the new site must come down:** point the DNS records back to the values written down in step A4 (the low TTL makes this take minutes to hours) and keep the old GoHighLevel site as it was until the move is stable.
- **If pages must be hidden from search for a while:** set `LIVE = False`, rebuild, commit and push. Every page goes back to `noindex, nofollow`, and the builder removes the launch files it wrote (`sitemap.xml`, `robots.txt`, `CNAME`, `_redirects` and the `calculator.html` stub), so nothing from the live build is left behind. Know the side effect before using this: on GitHub Pages the `CNAME` file is where the custom domain is kept, so expect the real address to stop opening the site until `LIVE = True` is restored (check GitHub's custom-domain page first). It pauses search, not the site, and pages Google already holds leave its results slowly.

## F. Mistakes this checklist exists to prevent (from Google's and GitHub's own guidance)

- Going live with the old `noindex, nofollow` still on every page, or leaving `Disallow: /` or a staging block behind.
- Canonicals or the sitemap still pointing at the github.io address.
- Deleting or replacing email DNS records while changing the web records.
- The build script deleting `CNAME`, `robots.txt` or `sitemap.xml` (the builder always writes them in a live build, and `tools/checkpoint.py` checks them).
- Redirecting everything to the home page (Google can treat that as a soft 404). Each old address should go to its closest new page; only addresses that are truly gone should return "not found".
- Redirect chains (apex to www to a stub to the real page).
- Changing addresses again right after launch.
- Forgetting that the "page not found" page must return a real 404 status on the real host (test a made-up address; if the host answers 200, tell Jeremy).

## Related files

- `research/hosting-decision.md`: the hosting choice, with sources.
- `research/site-map-proposal.md` (sections 10 to 13): the earlier thinking about search, the listing and switching the domain.
- `tools/seo-check.py`: the test for the preview and live builds.
- `ROADMAP.md`: decisions D9, D12, D13, D15, D17, D18.
