---
title: Los Vaqueros Reservoir
image: vaq.jpg
---

# Fishing Los Vaqueros Reservoir

Los Vaqueros Reservoir is a beautiful reservoir, set amidst towering turbines and golden rolling hills. In between Livermore and the Central Valley proper, it can be a long drive from the Bay Area but can provide excellent fishing at the right times. It is stocked with trout by the [DFW](https://nrm.dfg.ca.gov/fishplants/publicplantsearch?Params.StockingWaterID=27407&RegionCountyMappings=&submit=Search), and the [local management](https://www.ccwater.com/149/Fishing) plants trout and catfish. Native striped bass and largemouth bass also provide opportunities. <a href="#reports">See reports.</a>

<span style="color:red">This page is under construction, need to fish at this lake more ☺️ Please check back later for more info!</span>

{% include stocks_loc.html %}


## About the Lake

There are two main access points to Los Vaqueros. The first is from the south --- by following Los Vaqueros Road, you'll eventually get to the marina, where bait can be purchased and boats rented, and a parking lot provides a starting point to the southern half of the lake. The other alternative is Walnut Blvd from the north, which will put you right by the dam. 

Typically, the southern side is the more popular access, as the fish are stocked in the "South Cove". From South Cove to the marina, fishermen do well for trout and catfish, especially if you get the timing right after a plant. However, it can be very crowded, and the shore can be lined shoulder to shoulder with fishermen. It can also be quite windy on this side, so bring a jacket.

By following the Los Vaqueros Trail north from the marina, you can get some access to more peace and quiet, that dramatically increases the deeper you go into "Cowboy Cove". A couple of spots along the trail here can provide consistent action on striped bass and trout. Keep walking along the trail, and you'll eventually get to an oddly beautiful part of the lake, where flooded old trees provide cover to a wide variety of shorebirds. The water is shallow here, but it seems that the trout can congregate here at the right times.

![Flooded trees at Los Vaqueros](/assets/images/vaq_trees.jpg)
<div class="caption">Flooded trees at Los Vaqueros</div>

If you start from the northern side (or if you're willing to walk long enough from the south), you'll eventually get to so-called "Peninsula Cove", where you'll get access to a similarly quiet side of the lake. If you're fishing deep enough into the stocking season, fish will have made it over from South Cove and the fishing can be quite good thanks to the lack of pressure.

One alternative to all this hiking is renting a boat from the local concessionaire (no private boats are allowed). With a boat, you can not only fish all of the above areas, but you can also fish "Howden Cove" and other spots on the eastern side of the lake that are closed to shore fishermen thanks to the wind turbines. This again can make for good fishing, even without a recent plant.

For the striped bass, seems like the bait of choice here is cut anchovy.

There are also some big largemouth bass in this lake --- you can hunt them down in the less fished areas. Your classic bass baits should do the trick.


## Notes

The management charges both a $6 parking fee and a $6 fishing fee. Expensive, but can be worth it if you can find the fish.

[Check out my Bay Area trout fishing guide](/trout).

## Recommended Gear

{% include _gear/trout.html %}
{% include _gear/bass.html %}
{% include _gear/disclaimer.html %}
{% include _ads/article.html %}

<div id="reports"></div>

# Recent Reports 
{% assign sorted = site.reports | reverse %}
{% for report in sorted %}
{% if report.location == page.slug %}
<h3><a href="{{ report.url }}">{{ report.title }}</a></h3>
<h4>{{ report.date | date_to_string }}</h4>
<p>{{ report.content | markdownify }}</p>
{% endif %}
{% endfor %}


{% include _comments/fb.html %}