---
title: Shadow Cliffs Reservoir
image: shadowcliffs.webp
---

# Fishing Shadow Cliffs

Shadow Cliffs Reservoir is a converted gravel quarry that is stocked with trout and catfish by the [DFW](https://nrm.dfg.ca.gov/fishplants/publicplantsearch?Params.StockingWaterID=27417&RegionCountyMappings=&submit=Search) and [EBRPD](https://www.ebparks.org/recreation/fishing/anglers-edge-online). There are a few bass ponds within the park that provide additional fishing. <a href="#reports">See reports.</a>

<span style="color:red">This page is under construction, need to fish at this lake more ☺️ Please check back later for more info!</span>


## About the Lake

The reservoir does not really have a huge amount of fishable shoreline. Much of the land by the lake is not owned by the park, and a significant part of the main trail is closed thanks to storm damage. That means that in peak trout season, the lake can be quite crowded. 

People seem to do ok off the docks here using [Powerbait](https://amzn.to/3thy8dM){:target="_blank"} --- some hot spots are the second dock, the bench to the left of the boat ramp, and the Stanley Blvd shoreline. Cast as far as you can to get to the deeper water. The water can be quite shallow from the swim beach to the first dock, but the stocked trout can congregate here if they are freshly planted --- throw a [minijig](https://amzn.to/3pqIyHL){:target="_blank"} or a [spoon](https://amzn.to/3agKmui){:target="_blank"} for a few casts, and move on. It is extremely snaggy here though, so be wary. They also seem to show up on occasion in the really shallow water to the left of the swim beach, for whatever reason --- people will wade out and cast at them (at your own risk --- there are no wading signs littered throughout the park). 

The third dock gives you access to a mix of shallow and deep water that can provide action on occasion. Following the third dock, there is a small fisherman's trail that goes to the end of the reservoir where it gets extremely deep, but it's quite hard to fish thanks to overhanging foliage and the lack of flat ground --- if you wear good boots, you might be able to get a little bit of privacy here.

There are some big resident bass. There are also catfish that are planted in the main reservoir as well --- apparently the fishing can be quite good after trout plants, as they supposedly feed on the crawdads that in turn feed on dead stocked trout. 

The back ponds provide an option if the fishing at the main lake is slow. They've been full of weeds at the spots I've tried, but the fishing has been decent for bass and some large bluegill --- try to stick to weedless gear.

## Notes

The EBPRD charges both a $6 parking fee (more than Quarry), as well as a $5 fishing fee. Expensive, but can be worth it if you can find the fish. You can park outside and walk in, but make sure to buy a fishing permit.

Official website: [EBPRD](https://www.ebparks.org/parks/shadow-cliffs){:target="_blank"}

Fish plants and somewhat biased fishing reports: [Angler's Edge](https://www.ebparks.org/recreation/fishing/anglers-edge-online){:target="_blank"}

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