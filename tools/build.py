#!/usr/bin/env python3
"""Generates the static pages for the High Road Gallery proof of concept.
Run from the repo root: python3 tools/build.py
Shared header, menu, footer and CTA live here so every page stays in sync."""
import html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = "https://images.squarespace-cdn.com/content/v1/60a6fc39a488335a66e15a29/1623433898229-9FUAFWD6F3JUODGOEN4M/hrgsmlwrds_500px.jpg?format=500w"
HERO = "https://images.squarespace-cdn.com/content/v1/60a6fc39a488335a66e15a29/199ad8e4-bc71-4a28-a81e-54452d47fc45/IMG_4050.jpg?format=1000w"
MAPS = "https://www.google.com/maps/search/?api=1&query=12+E+Stafford+Worthington+OH+43085"

NAV = [("events", "Events"), ("gallery", "Gallery"), ("artists", "Artists"),
       ("classes", "Classes"), ("getinvolved", "Get Involved"), ("visit", "Visit")]
MORE = [("about", "About"), ("impact", "Impact"), ("press", "Press and praise")]

ARROW = '<svg class="icon card__arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
ICONS = {
    "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "img": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/>',
    "people": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
}

def icon(name):
    return '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % ICONS[name]

def card(href, title, text, ic="cal"):
    return ('<li><a class="card" href="%s"><span class="card__icon">%s</span><span>'
            '<span class="card__title">%s</span><span class="card__text">%s</span></span>%s</a></li>'
            % (href, icon(ic), title, text, ARROW))

def static_card(title, text, ic="cal"):
    return ('<li class="card card--static"><span class="card__icon">%s</span><span>'
            '<span class="card__title">%s</span><span class="card__text">%s</span></span><span></span></li>'
            % (icon(ic), title, text))

def ph(label, ratio="16-10"):
    return '<div class="ph ph--%s" role="img" aria-label="%s"><span>%s</span></div>' % (ratio, html.escape(label), html.escape(label))

def field(fid, label, kind="text", required=True, extra=""):
    req = " required" if required else ""
    if kind == "textarea":
        ctl = '<textarea id="%s" name="%s" rows="5"%s></textarea>' % (fid, fid, req)
    elif kind == "select":
        ctl = '<select id="%s" name="%s"%s>%s</select>' % (fid, fid, req, extra)
    else:
        ctl = '<input id="%s" name="%s" type="%s"%s autocomplete="%s">' % (
            fid, fid, kind, req, {"email": "email", "text": "off", "tel": "tel", "url": "url"}.get(kind, "off"))
    return '<div class="field"><label for="%s">%s</label>%s</div>' % (fid, label, ctl)

def form(fid, title, fields, submit, note=""):
    return ('<form class="form" id="%s" novalidate data-demo-form><h2 class="form__title">%s</h2>%s%s'
            '<button class="btn btn--primary" type="submit">%s</button>'
            '<p class="form__status" role="status" aria-live="polite" hidden></p></form>'
            % (fid, title, "".join(fields), ('<p class="form__note">%s</p>' % note) if note else "", submit))

def head(eyebrow, title, intro="", cta=None):
    btn = ('<p class="page-head__cta"><a class="btn btn--primary" href="%s">%s</a></p>' % cta) if cta else ""
    return ('<section class="page-head"><div class="container"><p class="eyebrow">%s</p><h1>%s</h1>%s%s</div></section>'
            % (eyebrow, title, ('<p class="page-head__lead">%s</p>' % intro) if intro else "", btn))

def split_section(title, left, right, tone="", sid=""):
    return ('<section class="section %s"%s><div class="container split"><div class="split__copy"><h2 class="section__title">%s</h2>%s</div>%s</div></section>'
            % (tone, (' id="%s"' % sid) if sid else "", title, left, right))

def section(title, body, tone="", sid=""):
    return ('<section class="section %s"%s><div class="container"><h2 class="section__title">%s</h2>%s</div></section>'
            % (tone, (' id="%s"' % sid) if sid else "", title, body))

def chrome(slug, title, desc, body):
    def link(s, t, cls="site-nav__link"):
        cur = ' aria-current="page"' if s == slug else ""
        return '<a class="%s" href="%s.html"%s>%s</a>' % (cls, s, cur, t)
    inline = "".join(link(s, t) for s, t in NAV)
    drawer = "".join(link(s, t) for s, t in NAV)
    more = "".join(link(s, t) for s, t in MORE)
    def col(cid, heading, items):
        lis = "".join('<li>%s</li>' % link(s, t, "site-footer__link") for s, t in items)
        return '<nav class="site-footer__col" aria-labelledby="%s"><p class="site-footer__title" id="%s">%s</p><ul>%s</ul></nav>' % (cid, cid, heading, lis)
    cols = (col("f-explore", "Explore", [("gallery", "Gallery"), ("artists", "Artists"), ("events", "Events")])
            + col("f-involved", "Get involved", [("classes", "Classes"), ("getinvolved", "Get Involved")])
            + col("f-visit", "Plan your visit", [("visit", "Visit"), ("about", "About")]))
    home = "./" if slug == "index" else "index.html"
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>%(title)s | High Road Gallery &amp; Studios</title>
  <meta name="description" content="%(desc)s">
  <meta name="theme-color" content="#FFFFFF">
  <meta name="color-scheme" content="light">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="icon" href="assets/icons/icon-192.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/icons/icon-192.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&amp;family=DM+Serif+Display&amp;display=swap">
  <link rel="stylesheet" href="assets/css/tokens.css">
  <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container site-header__inner">
      <a class="brand" href="%(home)s" aria-label="High Road Gallery &amp; Studios, home">
        <img class="brand__logo" src="%(logo)s" alt="" width="48" height="48">
        <span class="brand__name">High Road Gallery<span>&amp; Studios</span></span>
      </a>
      <nav class="nav-inline" aria-label="Primary">%(inline)s</nav>
      <div class="site-header__cta"><a class="btn btn--primary" href="contact.html"%(ccur)s>Contact</a></div>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="Menu">
        <svg class="icon icon--open" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
        <svg class="icon icon--close" viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>
      </button>
    </div>
  </header>
  <nav class="site-nav" id="site-menu" aria-label="Main menu">
    <div class="site-nav__group site-nav__group--primary">%(drawer)s</div>
    <div class="site-nav__group"><p class="site-nav__label">More</p>%(more)s</div>
    <div class="site-nav__actions">
      <a class="btn btn--primary" href="contact.html">Contact</a>
      <a class="btn btn--secondary" href="gallery.html#apply">Apply to Exhibit</a>
    </div>
  </nav>
  <main id="main">
%(body)s
  </main>
  <footer class="site-footer">
    <div class="container">
      <div class="site-footer__grid">
        <div class="site-footer__brand">
          <p class="site-footer__title">High Road Gallery &amp; Studios</p>
          <address>12 E Stafford<br>Worthington, Ohio 43085<br>Fridays and Saturdays, 12 to 4</address>
          <ul class="social">
            <li><a class="social__link" href="https://instagram.com/highroadgallery" aria-label="Instagram"><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/></svg></a></li>
            <li><a class="social__link" href="https://facebook.com/highroadgallery" aria-label="Facebook"><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a></li>
          </ul>
        </div>
        %(cols)s
      </div>
      <p class="site-footer__legal">&copy; <span id="year">2026</span> High Road Gallery &amp; Studios. A 501(c)3 non-profit artist collective. Design proof of concept.</p>
    </div>
  </footer>
  <div class="cta-bar" role="region" aria-label="Quick action"><a class="btn btn--primary" href="gallery.html#apply">Apply to Exhibit</a></div>
  <script src="assets/js/main.js" defer></script>
</body>
</html>
""" % dict(title=title, desc=html.escape(desc), home=home, logo=LOGO, inline=inline, drawer=drawer, more=more,
           cols=cols, body=body, ccur=' aria-current="page"' if slug == "contact" else "")

PAGES = {}

# HOME
PAGES["index"] = ("Home", "A non-profit artist collective in a historic 1818 home in Worthington, Ohio. Events, gallery, resident artists, classes and studio space.", """
    <section class="hero" aria-labelledby="hero-title">
      <div class="container hero__grid">
        <div>
          <p class="eyebrow">Non-profit artist collective</p>
          <h1 id="hero-title">Art can make community.</h1>
          <p class="hero__lead">High Road Gallery &amp; Studios is a historic 1818 home in Worthington, Ohio where artists create, exhibit and connect with their neighbors.</p>
          <div class="hero__actions">
            <a class="btn btn--primary" href="visit.html">Plan your visit</a>
            <a class="btn btn--secondary" href="events.html">See events</a>
          </div>
        </div>
        <figure class="hero__media"><img src="%s" alt="High Road Gallery &amp; Studios in Worthington, Ohio" width="1000" height="618" fetchpriority="high"></figure>
      </div>
    </section>
    <section aria-label="Visit information"><div class="container"><div class="visit">
      <div class="visit__item">%s<div><p class="visit__title">Open Fridays and Saturdays</p><p class="visit__text">12 to 4</p></div></div>
      <div class="visit__item">%s<div><p class="visit__title">12 E Stafford</p><p class="visit__text">Worthington, Ohio 43085</p></div></div>
      <a class="visit__link" href="%s">Get directions</a>
    </div></div></section>
    %s
    <section class="section" aria-labelledby="support-title"><div class="container"><div class="panel">
      <div><p class="eyebrow">Get involved</p><h2 class="section__title" id="support-title">This place matters.</h2>
      <p class="panel__body">Across the country, community art spaces are quietly disappearing. This one is still here, serving artists, neighbors and the next generation.</p>
      <p class="panel__body">Your tax-deductible gift helps preserve a historic building, keep studio spaces affordable and keep exhibitions open. We are an artist-run 501(c)3.</p></div>
      <div class="panel__actions"><a class="btn btn--primary" href="getinvolved.html">Get involved</a><a class="btn btn--secondary" href="getinvolved.html#donate">Donate</a></div>
    </div>
    <p class="thanks"><strong>Thank you</strong> to the Columbus Foundation for the grants and to Tilton Automotive for the donation. We are proud to be part of the America 250 celebration.</p></div></section>
    <section class="section" aria-labelledby="exhibit-title"><div class="container"><div class="panel">
      <div><p class="eyebrow">For artists</p><h2 class="section__title" id="exhibit-title">Show your work at High Road.</h2>
      <p class="panel__body">We keep studio space affordable and exhibiting accessible to emerging and established artists alike.</p></div>
      <div class="panel__actions"><a class="btn btn--primary" href="gallery.html#apply">Apply to Exhibit</a></div>
    </div></div></section>""" % (
    HERO, icon("clock"), icon("pin"), MAPS,
    section("Explore", '<ul class="cards">%s</ul>' % "".join([
        card("events.html", "Events", "Openings, shows and community days.", "cal"),
        card("gallery.html", "Gallery", "Current, coming up and past exhibits.", "img"),
        card("artists.html", "Artists", "Meet the artists working in our studios.", "people"),
        card("classes.html", "Classes", "Learn something new, at any level.", "book")]), sid="explore-title")))

# EVENTS
vi = lambda ic, t, d: '<div class="visit__item">%s<div><p class="visit__title">%s</p><p class="visit__text">%s</p></div></div>' % (icon(ic), t, d)
def ev_card(title, text, href="event.html", extra=""):
    return ('<li class="ev-card"%s><a class="ev-card__link" href="%s">%s<span class="ev-card__body"><span class="ev-card__text">'
            '<span class="card__title">%s</span><span class="card__text">%s</span></span>%s</span></a></li>'
            % (extra, href, ph("Event image"), title, text, ARROW))

def ev_list(items, more_id):
    shown = "".join(ev_card(t, d) for t, d in items[:3])
    hidden = "".join(ev_card(t, d, extra=" hidden data-more-item=\"%s\"" % more_id) for t, d in items[3:])
    return '<ul class="ev-cards">%s%s</ul>' % (shown, hidden)

up = [("Event title %d" % i, "Date and a short description.") for i in range(1, 6)]
past = [("2025", "Archive of past events."), ("2024", "Archive of past events."), ("2023", "Archive of past events."), ("2022", "Archive of past events.")]
PAGES["events"] = ("Events", "Upcoming events first. Past events live in the archive.",
    head("Events", "Events", "Upcoming events first. Past events are in the archive.")
    + section("Upcoming", ev_list(up, "up") + '<p class="center"><button class="btn btn--outline" type="button" data-more="up" aria-expanded="false">View more</button></p>')
    + section("Past events", '<ul class="past-cards">%s</ul><p class="center"><button class="btn btn--outline" type="button" data-more="past" aria-expanded="false">View archive</button></p>' % "".join(
        static_card(t, d) if i < 3 else static_card(t, d).replace('<li class="card', '<li hidden data-more-item="past" class="card', 1) for i, (t, d) in enumerate(past))))

# EVENT SPOTLIGHT
PAGES["event"] = ("Event spotlight", "Details for a High Road Gallery event: date, place and how to add it to your calendar.",
    head("Events", "Event title", "One short line about the event. Placeholder.")
    + '<section class="section"><div class="container">%s</div></section>' % ph("Event hero image", "16-10")
    + section("Details", '<div class="visit-grid">%s%s%s%s</div>' % (
        vi("cal", "Date", "Friday, January 9"), vi("clock", "Time", "5 to 9 pm"),
        vi("pin", "Location", "12 E Stafford, Worthington, OH"), vi("heart", "Cost", "Free")), "section--tint")
    + section("About this event", "<p>Placeholder copy. Describe the event, the artists and what to expect.</p>"
        '<p class="btn-row"><button class="btn btn--primary" type="button" data-ics>Add to calendar</button> '
        '<a class="btn btn--secondary" href="visit.html">Get directions</a></p>')
    + section("More events", ev_list([("Event title 2", "Date and a short description."), ("Event title 3", "Date and a short description.")], "x")
        + '<p class="center"><a class="btn btn--outline" href="events.html">View all events</a></p>', "section--tint"))

# GALLERY
gal_steps = '<ol class="steps"><li><strong>Review the requirements.</strong> What we show and how it works.</li><li><strong>Submit the application.</strong> Use the form below.</li><li><strong>We reply by email.</strong> Timeline to be confirmed.</li></ol>'
PAGES["gallery"] = ("Gallery", "Current, upcoming and past exhibits at High Road Gallery.",
    head("Gallery", "Gallery", "Current, upcoming and past exhibits.", ("#apply", "Apply to exhibit"))
    + split_section("On view now", '<h3>Exhibit title</h3><p>Dates and artists. Placeholder copy.</p>', ph("Exhibit image"), "section--tint")
    + section("Coming soon", '<ul class="cards cards--2">%s</ul>' % static_card("Exhibit title", "Opening date and artists.", "img"))
    + section("Past exhibits", '<ul class="cards cards--wide">%s</ul>' % "".join(static_card("Exhibit title", "Dates.", "img") for _ in range(3)), "section--tint")
    + '<section class="section" id="apply"><div class="container split split--top"><div class="split__copy"><h2 class="section__title">Apply to exhibit</h2>%s</div>%s</div></section>' % (
        gal_steps, form("form-apply", "Exhibit application", [field("a-name", "Name"), field("a-email", "Email", "email"), field("a-link", "Link to your work", "url"), field("a-msg", "About your work", "textarea")], "Submit application")))

# ARTISTS
art = "".join('<li class="artist">%s<h3>Artist name</h3><p>Medium. <a href="#artists-title">View profile</a></p></li>' % ph("Artist photo", "4-3") for _ in range(4))
PAGES["artists"] = ("Artists", "Meet the resident artists working in the studios at High Road Gallery.",
    head("Artists", "Artists", "Artists are the engine of High Road. Intro copy comes from the deck.", ("#studio-space", "Apply for studio space"))
    + section("Resident artists", '<ul class="artist-grid">%s</ul>' % art, "section--tint", "artists-title")
    + section("Past residents", "<p>List of past residents. Placeholder.</p>")
    + '<section class="section section--tint" id="studio-space"><div class="container split split--top"><div class="split__copy"><h2 class="section__title">Studio space</h2><p>No studios are open right now. Join the interest list and we will email you when one is.</p></div>%s</div></section>' % (
        form("form-studio", "Studio space interest", [field("s-name", "Name"), field("s-email", "Email", "email"), field("s-medium", "Medium and needs", "textarea")], "Join the list")))

# CLASSES
cls = ""
for t, d, fid in [("Private lessons", "One on one with a resident artist.", "private"), ("Art and tech lessons", "Digital and traditional work.", "tech"), ("Collage and Conversation", "Paused for now.", "collage")]:
    cls += ('<li class="class"><div class="card card--static"><span class="card__icon">%s</span><span><span class="card__title">%s</span><span class="card__text">%s</span></span><span></span></div>%s</li>'
            % (icon("book"), t, d, ('<a class="btn btn--secondary" href="#lessons-%s">Apply for lessons</a>' % fid) if fid != "collage" else ""))
forms = ""
for t, fid in [("Private lessons", "private"), ("Art and tech lessons", "tech")]:
    forms += '<div id="lessons-%s">%s</div>' % (fid, form("form-" + fid, "Apply for lessons: " + t,
        [field(fid + "-name", "Name"), field(fid + "-email", "Email", "email"), field(fid + "-msg", "Message", "textarea")],
        "Send application", "Goes to the instructor for this class. One form per class."))
PAGES["classes"] = ("Classes", "Classes with resident artists. Apply for lessons and the instructor replies.",
    head("Classes", "Classes", "Learn from resident artists. Apply for lessons and the instructor replies.", ("#lessons", "Apply for lessons"))
    + section("Offerings", '<ul class="class-list">%s</ul>' % cls, "section--tint")
    + '<section class="section" id="lessons"><div class="container forms-grid">%s</div></section>' % forms)

# GET INVOLVED
amounts = "".join('<button class="amount" type="button" aria-pressed="false" data-amount="%s">%s</button>' % (a, a) for a in ["$25", "$50", "$100", "Other"])
PAGES["getinvolved"] = ("Get Involved", "Donate, partner, sponsor and outreach at High Road Gallery.",
    head("Get Involved", "Get involved", "Donate, partner, sponsor and outreach in one place.")
    + section("Our mission", '<div class="prose"><p>High Road Gallery is a community art space where artists create, exhibit and connect. In our 1818 historic home, we support both emerging and established artists, offer a welcoming place for community connection and steward a meaningful piece of Worthington\'s history.</p><p><strong>Vision.</strong> We envision our historic 1818 home continuing to serve as a place where artists and community members gather to nurture beauty and belonging.</p><p>Your gift keeps this place open to artists and the community.</p></div>')
    + section("Donate", '<p class="panel__body">Gifts are tax-deductible. We are an artist-run 501(c)3.</p><div class="amounts" role="group" aria-label="Donation amount">%s</div><p><button class="btn btn--primary" type="button" data-donate>Donate</button></p><p class="form__status" role="status" aria-live="polite" data-donate-status hidden></p><p class="panel__note">Prefer to mail a check? Make it out to High Road Gallery and send it to 12 East Stafford, Worthington, Ohio 43085.</p>' % amounts, "section--tint", "donate")
    + section("Why give", '<ul class="cards cards--2">%s%s</ul>' % (static_card("Building needs", "What the 1818 building requires.", "heart"), static_card("What gifts fund", "Preserve, support and give access.", "heart")))
    + section("Partner and sponsor", '<ul class="cards cards--2">%s</ul>' % "".join(static_card(t, "One line description. Placeholder.", "people") for t in ["Sponsorships", "Grants", "Multi-year support", "Building gifts"]), "section--tint")
    + split_section("Outreach", "<p>Schools, public art and inclusive programs.</p>", ph("Outreach image"))
    + section("Our friends", '<p>Thank you to the Columbus Foundation for the grants and to Tilton Automotive for the donation.</p><p><a class="btn btn--secondary" href="impact.html">See our impact</a></p>', "section--tint"))

# VISIT
PAGES["visit"] = ("Visit", "Hours, address and parking for High Road Gallery in Worthington, Ohio.",
    head("Visit", "Visit", "Plan your trip: when we are open and how to find us.")
    + section("Hours", '<div class="visit-grid">%s%s%s</div>' % (vi("clock", "Fridays and Saturdays", "12 to 4"), vi("clock", "Summer hours", "10 to 4, May to September. Check before you go."), vi("clock", "January closure", "Closed for the month. Check before you go.")), "section--tint")
    + split_section("Find us", '<address>12 E Stafford<br>Worthington, Ohio 43085</address><p><a class="btn btn--secondary" href="%s">Get directions</a></p>' % MAPS, ph("Map"))
    + section("Parking and access", "<p>Parking and accessibility details. Placeholder.</p>", "section--tint")
    + section("Groups and events", '<p>Planning a group visit or private event?</p><p><a class="btn btn--secondary" href="contact.html">Contact us</a></p>'))

# CONTACT
topics = "".join('<option>%s</option>' % t for t in ["General question", "Group visit", "Private event", "Press", "Other"])
PAGES["contact"] = ("Contact", "Contact High Road Gallery with questions, group events, private tours and press.",
    head("Contact", "Contact", "Questions, group events, private tours and press. Looking for hours or directions? <a href=\"visit.html\">Plan your visit</a>.")
    + '<section class="section section--tint"><div class="container split split--top">%s<div><h2 class="section__title">Reach us</h2><div class="visit-grid visit-grid--stack">%s%s%s</div></div></div></section>' % (
        form("form-contact", "Send a message", [field("c-topic", "Topic", "select", True, topics), field("c-name", "Name"), field("c-email", "Email", "email"), field("c-msg", "Message", "textarea")], "Send message"),
        vi("mail", "Email", "Placeholder address"), vi("people", "Social", '<a href="https://instagram.com/highroadgallery">Instagram</a>, <a href="https://facebook.com/highroadgallery">Facebook</a>'), vi("pin", "Mailing address", "12 E Stafford, Worthington, OH 43085")))

# ABOUT
tl = ""
for y in ["1818", "2001", "2024", "Today"]:
    tl += '<li class="timeline__item"><h3 class="timeline__year">%s</h3>%s<div><h4>Milestone title</h4><p>Placeholder copy. Replace with the slide wording.</p></div></li>' % (y, ph("Image placeholder"))
PAGES["about"] = ("About", "The story of High Road Gallery & Studios, from 1818 to today.",
    head("About", "Our story", "From 1818 to today.")
    + '<section class="section"><div class="container"><ol class="timeline">%s</ol></div></section>' % tl
    + section("What makes High Road distinct", "<p>Placeholder copy.</p>", "section--tint")
    + section("Mission and vision", "<p>Placeholder copy.</p>")
    + section("Board", "<p>Board list. Placeholder.</p>", "section--tint")
    + section("More", '<ul class="cards cards--wide">%s%s</ul>' % (card("impact.html", "Impact", "Results and reach since 2001.", "heart"), card("press.html", "Press and praise", "What people say about High Road.", "people"))))

PAGES["impact"] = ("Impact", "Results and reach since 2001.", head("About", "Impact", "Results and reach since 2001.") + section("By the numbers", "<p>Stats from the 2025 review. Placeholder.</p>", "section--tint"))
PAGES["press"] = ("Press and praise", "Press coverage and testimonials, written as text cards.", head("About", "Press and praise", "Text cards to be written. No screenshots.") + section("Coverage", "<p>Placeholder.</p>", "section--tint"))

for stale in ("apply.html", "partnerships.html"):
    try:
        os.remove(os.path.join(ROOT, stale))
    except FileNotFoundError:
        pass

for slug, (title, desc, body) in PAGES.items():
    with open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8") as f:
        f.write(chrome(slug, title, desc, body))
print("wrote", len(PAGES), "pages")
