"""The photos on the Our work page, in the order they appear. Each entry is one photo.

  group    "renovating" (houses being fixed up), "building" (new-construction job site) or "closed" (closings)
  img      the picture shown in the grid
  full     the larger picture shown in the photo viewer (leave it out when the grid picture is already the biggest we have)
  alt      what the photo shows, for people who can't see it. Describe only what is visible. No claims.
  caption  the short label on the photo. Plain facts only (the stage of the work, or the month for a closing).

To add a photo:
  1. Put the picture in research/photos/incoming/ and run   python3 tools/process-photos.py --slug NAME <file>
     (it shrinks the photo, removes the camera and location data, and prints the line to paste below).
  2. Paste the line here, in the order you want, set the group, and write the alt text and caption from what the photo shows.
  3. Add a row for it in CONTENT_CLAIMS.md: who took it, and whether the people in it agreed to be on the site.
  4. Run   python3 tools/build-pages.py
Width and height are read from the picture files when the page is built, so they can never disagree with the photo.
Photos with a person's face in them wait for Joey's OK. Never put a street address in a caption or alt text.
"""

GALLERY = [
    # ---- Renovating
    dict(group="renovating", img="images/work/reno-before-after.jpg",
         alt="Before and after of a house's back deck. On top, a deck covered in trash, old dark wood siding and a ladder against the doors. Below, the finished house with new gray siding, a new roof and a new wooden deck.",
         caption="Before and after"),
    dict(group="renovating", img="images/work/reno-studs-sm.jpg", full="images/work/reno-studs.jpg",
         alt="The inside of a house stripped down to the studs and joists, with a new row of framed wall studs in the foreground, large windows on the left and a worker bending over at the back.",
         caption="Down to the studs"),
    dict(group="renovating", img="images/work/reno-roof.jpg",
         alt="A brick ranch house with a roofer on the roof, a ladder against the eave and pallets of shingles stacked in the yard.",
         caption="New roof going on"),
    dict(group="renovating", img="images/work/reno-living-room.jpg",
         alt="A living room with lavender walls, two built-in shelves and an arched opening to a dining room, with the old wood floor still bare and a trash can in the corner.",
         caption="Mid-renovation"),
    dict(group="renovating", img="images/work/reno-kitchen-going-in.jpg",
         alt="A kitchen being installed: white shaker cabinets, speckled gray countertops, an island with shiplap-style paneling, and tools and cords on the wood-look floor.",
         caption="Kitchen going in"),
    dict(group="renovating", img="images/work/reno-kitchen-gray.jpg",
         alt="A kitchen with gray shaker cabinets, black pulls, a light countertop and a center island, with wood-look flooring.",
         caption="Kitchen with an island"),
    dict(group="renovating", img="images/work/reno-kitchen-white.jpg",
         alt="A kitchen with white shaker cabinets, white subway tile, speckled gray countertops, stainless steel appliances and wood-look flooring.",
         caption="White cabinets, subway tile"),
    dict(group="renovating", img="images/work/reno-exterior-sunset.jpg",
         alt="A single-story house with white-painted brick, a covered front porch with a cedar post and a dark gray front door, under a pink sunset sky, with lumber stacked in the yard.",
         caption="Painted brick and a cedar porch post"),

    # ---- Building (the new home on the New homes page, and its lot)
    dict(group="building", img="images/work/site-work-lot-sm.jpg", full="images/work/site-work-lot.jpg",
         alt="Bare, graded dirt on a hillside lot, with black silt fence along the edge, a gravel entrance on the right and tall pines behind",
         caption="Lot cleared and graded"),
    dict(group="building", img="images/work/site-work-gravel-entrance-sm.jpg", full="images/work/site-work-gravel-entrance.jpg",
         alt="A graded lot with a gravel entrance from the street, black silt fence along the edges and a compact track loader parked at the back",
         caption="Gravel entrance in"),
    dict(group="building", img="images/build-exterior.jpg",
         alt="The new two-story home with a covered front deck and stairs, under tall pines",
         caption="Decks on, siding going up"),
    dict(group="building", img="images/build-lot.jpg",
         alt="A mini excavator and a pile of gravel on the lot during site work",
         caption="Site work on the lot"),
    dict(group="building", img="images/build-driveway.jpg",
         alt="Crew pouring the concrete driveway in front of the new home",
         caption="Driveway pour"),
    dict(group="building", img="images/work/concrete-truck.jpg",
         alt="Freshly poured concrete next to a wooden deck, with a concrete mixer truck and a crew member in the background",
         caption="Fresh concrete"),
    dict(group="building", img="images/build-kitchen.jpg",
         alt="Kitchen with new shaker cabinets installed and floors protected during construction",
         caption="Kitchen cabinets in"),

    # ---- Recently closed
    dict(group="closed", img="images/closing-day.jpg",
         alt="Closing day: Joey with the homeowners at the title office, holding a Just Closed key and a GLP Home Options sign",
         caption="Closed · September 2026"),
    # Added Oct 21 (11:35 PM) on Jeremy's word ("this other picture would be perfect for this section").
    # NOT confirmed by Joey: who the two other people are, whether they and the title company agree to appear,
    # and when it was taken. The caption claims no date. See CONTENT_CLAIMS.md row 47 and the private log.
    dict(group="closed", img="images/work/closing-sold-sign.jpg",
         alt="Closing day: three people smiling in an office, holding a SOLD sign",
         caption="Another closing day"),
]
