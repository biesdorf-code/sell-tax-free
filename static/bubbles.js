/**
 * One bubble per lot (FR-005). X = acquisition date; same-day lots stack vertically.
 */
(function () {
  const root = document.getElementById("bubble-timeline");
  const dataEl = document.getElementById("bubble-lots-data");
  if (!root || !dataEl) return;

  let lots;
  try {
    lots = JSON.parse(dataEl.textContent);
  } catch {
    return;
  }
  if (!lots.length) {
    root.innerHTML = '<p class="muted">No lots to show.</p>';
    return;
  }

  const quantities = lots.map((l) => parseFloat(l.quantity, 10)).filter((q) => q > 0);
  const qMax = Math.max(...quantities, 1);
  const minR = 14;
  const maxR = 44;

  function radiusForQty(qty) {
    const t = Math.sqrt(qty / qMax);
    return minR + t * (maxR - minR);
  }

  const dates = lots.map((l) => new Date(l.lot_date + "T12:00:00"));
  const tMin = Math.min(...dates.map((d) => d.getTime()));
  const tMax = Math.max(...dates.map((d) => d.getTime()));
  const span = Math.max(tMax - tMin, 1);

  const pad = 8;
  function xPercentForTime(t) {
    if (tMax === tMin) return 50;
    return pad + ((t - tMin) / span) * (100 - 2 * pad);
  }

  const byDay = new Map();
  for (const lot of lots) {
    const key = lot.lot_date;
    if (!byDay.has(key)) byDay.set(key, []);
    byDay.get(key).push(lot);
  }
  for (const arr of byDay.values()) {
    arr.sort((a, b) => a.ticker.localeCompare(b.ticker));
  }

  let maxStack = 1;
  for (const arr of byDay.values()) {
    maxStack = Math.max(maxStack, arr.length);
  }
  const laneMin = 16 + maxStack * (maxR * 2 + 6) + 28;

  const lane = document.createElement("div");
  lane.className = "bubble-lane";
  lane.style.minHeight = laneMin + "px";
  root.appendChild(lane);

  const axis = document.createElement("div");
  axis.className = "bubble-axis";
  axis.setAttribute("aria-hidden", "true");
  lane.appendChild(axis);

  for (const lot of lots) {
    const t = new Date(lot.lot_date + "T12:00:00").getTime();
    const x = xPercentForTime(t);
    const siblings = byDay.get(lot.lot_date);
    const stackIndex = siblings.indexOf(lot);
    const qty = parseFloat(lot.quantity, 10);
    const r = radiusForQty(qty);

    const wrap = document.createElement("div");
    wrap.className = "bubble-wrap";
    wrap.style.left = x + "%";
    wrap.style.bottom = 16 + stackIndex * (maxR * 2 + 6) + "px";

    const bubble = document.createElement("button");
    bubble.type = "button";
    bubble.className = "bubble" + (lot.tax_free ? " bubble--free" : " bubble--wait");
    bubble.style.width = r * 2 + "px";
    bubble.style.height = r * 2 + "px";

    const status = lot.tax_free ? "Tax-free" : `${lot.days_until_tax_free} day(s) until tax-free`;
    const title =
      `${lot.ticker} — ${lot.quantity} shares — lot date ${lot.lot_date} — ${status}`;
    bubble.setAttribute("title", title);
    bubble.setAttribute(
      "aria-label",
      `${lot.ticker}, ${lot.quantity} shares, bought ${lot.lot_date}. ${status}. Click for confetti.`,
    );

    bubble.addEventListener("click", () => {
      if (typeof confetti === "function") {
        confetti({
          particleCount: 90,
          spread: 70,
          origin: { y: 0.65 },
        });
      }
    });

    wrap.appendChild(bubble);
    lane.appendChild(wrap);
  }

  const dayKeys = [...byDay.keys()].sort();
  const minLabel = dayKeys[0];
  const maxLabel = dayKeys[dayKeys.length - 1];
  const legend = document.createElement("div");
  legend.className = "bubble-legend muted";
  legend.textContent =
    minLabel === maxLabel
      ? `Lot date: ${minLabel} (multiple lots stack vertically when same day).`
      : `Earlier ← ${minLabel} … ${maxLabel} → later`;
  root.appendChild(legend);
})();
