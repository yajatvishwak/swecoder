<script>
  import { onMount } from "svelte";

  // Props for customization
  // data supports either numeric values or objects with counters
  // { "2025-01-15": 5 } or { "2025-01-15": { submissions: 2, revisions: 3 } }
  export let data = {};
  export let startDate = null; // Start date for the calendar
  export let endDate = null; // End date for the calendar
  export let cellSize = 12; // Size of each cell in pixels
  export let cellGap = 3; // Gap between cells

  // Independent month blocks with their own weeks
  let monthsGrid = [];
  let hoveredCell = null;
  let tooltipLeft = 0;
  let tooltipTop = 0;

  // Helper function to format date in local timezone (YYYY-MM-DD)
  function formatDateLocal(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  }

  // Generate calendar data
  function generateCalendar() {
    const end = endDate ? new Date(endDate) : new Date();
    const start = startDate
      ? new Date(startDate)
      : new Date(end.getFullYear(), end.getMonth() - 8, 1); // Last 8 months

    monthsGrid = [];

    // Calculate the first day (Sunday) of the week containing start date
    const firstDay = new Date(start);
    firstDay.setDate(start.getDate() - start.getDay());

    // Build month blocks one by one so each month starts at its own grid
    let iter = new Date(start.getFullYear(), start.getMonth(), 1);
    const endMonth = new Date(end.getFullYear(), end.getMonth(), 1);
    while (iter <= endMonth) {
      const y = iter.getFullYear();
      const m = iter.getMonth();
      const monthStart = new Date(y, m, 1);
      const monthEnd = new Date(y, m + 1, 0);

      const leadingBlanks = monthStart.getDay();
      const daysInMonth = monthEnd.getDate();
      const totalCells = leadingBlanks + daysInMonth;
      const weeksCount = Math.ceil(totalCells / 7);

      const gridStart = new Date(monthStart);
      gridStart.setDate(monthStart.getDate() - leadingBlanks);

      const monthWeeks = [];
      const cursor = new Date(gridStart);
      for (let w = 0; w < weeksCount; w++) {
        const week = [];
        for (let i = 0; i < 7; i++) {
          const dateStr = formatDateLocal(cursor);
          const inMonth = cursor.getMonth() === m;
          const inRange = cursor >= start && cursor <= end;
          let submissions = 0;
          let revisions = 0;
          let value = 0;
          if (inMonth && inRange) {
            const entry = data[dateStr];
            if (typeof entry === "number") {
              value = entry;
            } else if (entry) {
              submissions = Number(entry.submissions) || 0;
              revisions = Number(entry.revisions) || 0;
              value = revisions; // Only count revisions for heat map
            }
          }
          week.push({
            date: new Date(cursor),
            dateStr,
            value,
            isInRange: inMonth && inRange,
            inMonth,
            submissions,
            revisions,
            dayOfWeek: i,
          });
          cursor.setDate(cursor.getDate() + 1);
        }
        monthWeeks.push(week);
      }

      monthsGrid.push({
        label: monthStart.toLocaleString("en-US", { month: "short" }),
        weeks: monthWeeks,
      });

      iter = new Date(y, m + 1, 1);
    }
  }

  // Get intensity level (0-4) based on value
  function getIntensity(value) {
    if (value === 0) return 0;
    if (value <= 2) return 1;
    if (value <= 4) return 2;
    if (value <= 6) return 3;
    return 4;
  }

  // Get color class based on intensity
  function getColorClass(intensity) {
    const colors = [
      "bg-base-300", // No activity
      "bg-primary opacity-20", // Low
      "bg-primary opacity-40", // Medium-low
      "bg-primary opacity-70", // Medium-high
      "bg-primary", // High
    ];
    return colors[intensity];
  }

  function handleCellHover(event, cell) {
    if (!cell.isInRange) return;
    hoveredCell = cell;
    const rect = event.currentTarget.getBoundingClientRect();
    tooltipLeft = rect.left + rect.width + 8; // to the right of cell
    tooltipTop = rect.top + rect.height / 2; // vertically centered
  }

  function handleCellLeave() {
    hoveredCell = null;
  }

  onMount(() => {
    generateCalendar();
  });

  // Regenerate when data or date range changes
  $: {
    data;
    startDate;
    endDate;
    generateCalendar();
  }

  // Day labels
  const dayLabels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
</script>

<div class="heatmap-container p-6">
  <div class="flex items-start gap-4">
    <!-- Day labels -->
    <div class="flex flex-col gap-[3px] text-xs text-base-content/60 pt-6">
      {#each dayLabels as day, i}
        {#if i % 2 === 1}
          <div style="height: {cellSize}px; line-height: {cellSize}px;">
            {day}
          </div>
        {:else}
          <div style="height: {cellSize}px;"></div>
        {/if}
      {/each}
    </div>

    <!-- Calendar grid -->
    <div class="flex-1">
      <!-- Month blocks -->
      <div class="flex gap-6">
        {#each monthsGrid as month}
          <div class="flex flex-col">
            <div class="mb-2 text-xs text-base-content/60 h-4">
              {month.label}
            </div>
            <div class="flex gap-[3px]">
              {#each month.weeks as week}
                <div class="flex flex-col gap-[3px]">
                  {#each week as cell}
                    <div
                      class="cell rounded-sm cursor-pointer transition-all hover:ring-2 hover:ring-primary/50 {cell.isInRange
                        ? getColorClass(getIntensity(cell.value))
                        : 'bg-base-200 opacity-30'} {cell.inMonth
                        ? ''
                        : 'opacity-30'}"
                      style="width: {cellSize}px; height: {cellSize}px;"
                      role="button"
                      tabindex="0"
                      on:mouseenter={(e) => handleCellHover(e, cell)}
                      on:mouseleave={handleCellLeave}
                      on:focus={(e) => handleCellHover(e, cell)}
                      on:blur={handleCellLeave}
                    ></div>
                  {/each}
                </div>
              {/each}
            </div>
          </div>
        {/each}
      </div>

      <!-- Legend -->
      <div class="flex items-center gap-2 mt-4 text-xs text-base-content/60">
        <span>Less</span>
        <div class="flex gap-1">
          {#each [0, 1, 2, 3, 4] as intensity}
            <div
              class="rounded-sm {getColorClass(intensity)}"
              style="width: {cellSize}px; height: {cellSize}px;"
            ></div>
          {/each}
        </div>
        <span>More</span>
      </div>
    </div>
  </div>

  <!-- Tooltip -->
  {#if hoveredCell}
    <div
      class="tooltip-container"
      style="left: {tooltipLeft}px; top: {tooltipTop}px;"
    >
      <div class="tooltip bg-base-300 p-2 rounded-md shadow-lg text-sm">
        <div class="font-semibold">
          {hoveredCell.date.toLocaleDateString("en-US", {
            weekday: "short",
            year: "numeric",
            month: "short",
            day: "numeric",
          })}
        </div>
        <div class="text-base-content/70 flex gap-4">
          <div>
            <span class="opacity-60">Submissions:</span>
            {hoveredCell.submissions || 0}
          </div>
          <div>
            <span class="opacity-60">Revisions:</span>
            {hoveredCell.revisions || 0}
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .heatmap-container {
    position: relative;
    max-width: 100%;
    overflow-x: auto;
  }

  .cell {
    border: 1px solid oklch(0% 0 0);
  }

  .month-separator {
    margin-left: 8px;
  }

  .tooltip-container {
    position: fixed;
    pointer-events: none;
    z-index: 1000;
    transform: translateY(-50%);
  }

  .tooltip {
    white-space: nowrap;
  }
</style>
