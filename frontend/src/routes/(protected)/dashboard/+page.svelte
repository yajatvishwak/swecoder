<script>
  import { logout } from "$lib/auth.js";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import HeatMap from "$lib/components/HeatMap.svelte";

  let today = new Date();
  let data = {};
  let solvedQuestions = [];
  let revisionQuestions = [];
  let searchQuery = "";
  let loadingRevisions = true;
  let loadingSolved = true;
  let loadingActivity = true;

  // Modal state
  let showModal = false;
  let leetcodeSlug = "";
  let submissionCode = "";
  let submitting = false;

  // Revision modal state
  let showRevisionModal = false;
  let revisionQuestion = null;
  let revisionCode = "";
  let revisionDifficulty = "";
  let submittingRevision = false;
  const difficulties = [
    { value: "easy", label: "Easy - I solved it quickly" },
    { value: "medium", label: "Medium - It took some thinking" },
    { value: "hard", label: "Hard - I struggled with it" },
  ];

  async function fetchActivity() {
    try {
      loadingActivity = true;
      const response = await fetch("/api/get-activity");
      if (response.ok) {
        const result = await response.json();
        // Create a new object reference to trigger Svelte reactivity
        data = { ...(result.data || {}) };
      } else {
        console.error("Failed to fetch activity data");
      }
    } catch (error) {
      console.error("Failed to fetch activity data:", error);
    } finally {
      loadingActivity = false;
    }
  }

  async function fetchRevisionQuestions() {
    try {
      loadingRevisions = true;
      const response = await fetch("/api/get-revision-questions");
      if (response.ok) {
        const data = await response.json();
        revisionQuestions = data.items || [];
      } else {
        console.error("Failed to fetch revision questions");
      }
    } catch (error) {
      console.error("Failed to fetch revision questions:", error);
    } finally {
      loadingRevisions = false;
    }
  }

  async function fetchSolvedQuestions() {
    try {
      loadingSolved = true;
      const response = await fetch("/api/get-solved-questions");
      if (response.ok) {
        const data = await response.json();
        solvedQuestions = data.items || [];
      } else {
        console.error("Failed to fetch solved questions");
      }
    } catch (error) {
      console.error("Failed to fetch solved questions:", error);
    } finally {
      loadingSolved = false;
    }
  }

  onMount(() => {
    setInterval(() => {
      today = new Date();
    }, 1000);
    fetchActivity();
    fetchRevisionQuestions();
    fetchSolvedQuestions();
  });

  $: hour24 = today.getHours();
  $: hour12 = hour24 % 12 || 12;
  $: ampm = hour24 >= 12 ? "PM" : "AM";
  $: hh = String(hour12).padStart(2, "0");
  $: mm = String(today.getMinutes()).padStart(2, "0");
  $: dd = String(today.getDate()).padStart(2, "0");
  $: mon = today.toLocaleString("en-US", { month: "short" });
  $: yyyy = today.getFullYear();
  $: dateStr = `${mon} ${dd}, ${yyyy}`;

  $: filteredQuestions = solvedQuestions.filter((q) =>
    q.problem_title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  async function handleSubmit() {
    if (!leetcodeSlug.trim() || !submissionCode.trim()) {
      alert("Please fill in both fields");
      return;
    }

    try {
      submitting = true;
      const response = await fetch("/api/store-submission", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          leetcode_slug: leetcodeSlug.trim(),
          code: submissionCode.trim(),
        }),
      });

      if (response.ok) {
        const result = await response.json();
        // Reset form
        leetcodeSlug = "";
        submissionCode = "";
        showModal = false;

        // Refresh data
        fetchActivity();
        fetchRevisionQuestions();
        fetchSolvedQuestions();

        alert(
          result.created_problem
            ? "New problem submitted successfully!"
            : "Submission recorded!"
        );
      } else {
        const errorData = await response.json();
        alert(errorData.error || "Failed to submit code");
      }
    } catch (error) {
      console.error("Submission error:", error);
      alert("Failed to submit code");
    } finally {
      submitting = false;
    }
  }

  function openRevisionModal(question) {
    revisionQuestion = question;
    revisionCode = "";
    revisionDifficulty = "";
    showRevisionModal = true;
  }

  async function handleRevisionSubmit() {
    if (!revisionCode.trim()) {
      alert("Please enter your code");
      return;
    }

    if (!revisionDifficulty) {
      alert("Please select a difficulty level");
      return;
    }

    try {
      submittingRevision = true;
      const response = await fetch("/api/store-submission", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          leetcode_slug: revisionQuestion.leetcode_slug,
          problem_title: revisionQuestion.problem_title,
          code: revisionCode.trim(),
          difficulty: revisionDifficulty,
          is_revision: true,
        }),
      });

      if (response.ok) {
        // Reset form
        revisionCode = "";
        revisionDifficulty = "";
        revisionQuestion = null;
        showRevisionModal = false;

        // Refresh data
        fetchActivity();
        fetchRevisionQuestions();
        fetchSolvedQuestions();

        alert("Revision submitted successfully!");
      } else {
        const errorData = await response.json();
        alert(errorData.error || "Failed to submit revision");
      }
    } catch (error) {
      console.error("Revision submission error:", error);
      alert("Failed to submit revision");
    } finally {
      submittingRevision = false;
    }
  }

  function formatDate(dateString) {
    const date = new Date(dateString);
    const mon = date.toLocaleString("en-US", { month: "short" });
    const day = String(date.getDate()).padStart(2, "0");
    const year = date.getFullYear();
    return `${mon} ${day}, ${year}`;
  }

  function handleLogout() {
    logout();
    goto("/login");
  }
</script>

<div class="h-[93svh] w-full flex flex-col">
  {@render navbar()}
  <div class="">
    {#if loadingActivity}
      <div class="flex justify-center items-center py-12">
        <span class="loading loading-spinner loading-lg"></span>
      </div>
    {:else}
      <HeatMap {data}></HeatMap>
    {/if}
    <div class="mt-6">
      <div class="font-semibold mb-2 opacity-70">Today's Revision</div>
      <div class="overflow-x-auto">
        <table class="table">
          <thead>
            <tr>
              <th class="text-sm font-normal border-2 border-base-200"
                >Question name</th
              >
              <th class="text-sm font-normal border-2 border-base-200"
                >Last attempted on</th
              >
              <th class="text-sm font-normal border-2 border-base-200"
                >Status</th
              >
              <th class="text-sm font-normal border-2 border-base-200"
                >Late by</th
              >
              <th class="text-sm font-normal border-2 border-base-200">Stage</th
              >
              <th class="text-right bg-base-200">Action</th>
            </tr>
          </thead>
          <tbody>
            {#if loadingRevisions}
              <tr>
                <td colspan="6" class="text-center py-8">
                  <span class="loading loading-spinner loading-lg"></span>
                </td>
              </tr>
            {:else if revisionQuestions.length === 0}
              <tr>
                <td colspan="6" class="text-center py-8 opacity-50">
                  No revisions pending today
                </td>
              </tr>
            {:else}
              {#each revisionQuestions as question}
                <tr>
                  <td>{question.problem_title}</td>
                  <td
                    >{question.last_attempted_at
                      ? formatDate(question.last_attempted_at)
                      : "N/A"}</td
                  >
                  <td>{question.status}</td>
                  <td>{question.late_by}</td>
                  <td>{question.stage}</td>
                  <td class="text-right">
                    <!-- change popover-1 and --anchor-1 names. Use unique names for each dropdown -->
                    <button
                      class="btn"
                      popovertarget="popover-1"
                      style="anchor-name:--anchor-1"
                    >
                      Button
                    </button>
                    <ul
                      class="dropdown menu w-52 dropdown-end rounded-box bg-base-200 shadow-sm"
                      popover
                      id="popover-1"
                      style="position-anchor:--anchor-1"
                    >
                      <li>
                        <a
                          href={`https://leetcode.com/problems/${question.leetcode_slug}/`}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          Open on LeetCode
                        </a>
                      </li>
                      <li>
                        <button on:click={() => openRevisionModal(question)}>
                          Submit Revision
                        </button>
                      </li>
                    </ul>
                  </td>
                </tr>
              {/each}
            {/if}
          </tbody>
        </table>
      </div>
    </div>

    <div class="mt-6">
      <div class="flex justify-between gap-2">
        <div class="font-semibold mb-2 opacity-70 flex items-center gap-2">
          Solved Questions
          <span class="badge badge-primary">{solvedQuestions.length}</span>
        </div>
        <div class="mb-">
          <input
            type="text"
            placeholder="Search questions..."
            class="input input-bordered w-full max-w-xs"
            bind:value={searchQuery}
          />
        </div>
      </div>
      <div class="overflow-x-auto mt-2">
        <table class="table">
          <thead>
            <tr>
              <th class="text-sm font-normal border-2 border-base-200"
                >Question name</th
              >
              <th class="text-sm font-normal border-2 border-base-200"
                >Date solved</th
              >
              <th class="text-sm font-normal border-2 border-base-200"
                >Total attempts</th
              >
              <th class="text-right bg-base-200">Action</th>
            </tr>
          </thead>
          <tbody>
            {#if loadingSolved}
              <tr>
                <td colspan="4" class="text-center py-8">
                  <span class="loading loading-spinner loading-lg"></span>
                </td>
              </tr>
            {:else if filteredQuestions.length === 0}
              <tr>
                <td colspan="4" class="text-center py-8 opacity-50">
                  {searchQuery
                    ? "No questions found"
                    : "No solved questions yet"}
                </td>
              </tr>
            {:else}
              {#each filteredQuestions as question}
                <tr>
                  <td>{question.problem_title}</td>
                  <td>{formatDate(question.first_solved_date)}</td>
                  <td>{question.attempts}</td>
                  <td class="text-right">
                    <a
                      href={`https://leetcode.com/problems/${question.leetcode_slug}/`}
                      target="_blank"
                      rel="noopener noreferrer"
                      class="btn btn-sm btn-primary"
                    >
                      Open
                    </a>
                  </td>
                </tr>
              {/each}
            {/if}
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <!-- Floating Action Button -->
  {@render fab()}
</div>

<!-- Submit Code Modal -->
<input
  type="checkbox"
  id="submit_modal"
  class="modal-toggle"
  bind:checked={showModal}
/>
<div class="modal" role="dialog">
  <div class="modal-box bg-base-200">
    <h3 class="font-bold text-lg mb-4">Submit Your Code</h3>
    <form on:submit|preventDefault={handleSubmit}>
      <div class="form-control mb-4">
        <label class="label" for="leetcode_slug_input">
          <span class="label text-sm mb-1">LeetCode Question Slug</span>
        </label>
        <input
          id="leetcode_slug_input"
          type="text"
          placeholder="e.g., two-sum"
          class="input input-bordered w-full"
          bind:value={leetcodeSlug}
          disabled={submitting}
          required
        />
      </div>

      <div class="form-control mb-4">
        <label class="label" for="submission_code_input">
          <span class="label text-sm mb-1">Your Code</span>
        </label>
        <textarea
          id="submission_code_input"
          placeholder="Paste your solution here..."
          class="textarea textarea-bordered w-full h-64"
          bind:value={submissionCode}
          disabled={submitting}
          required
        ></textarea>
      </div>

      <div class="modal-action">
        <button type="submit" class="btn btn-primary" disabled={submitting}>
          {#if submitting}
            <span class="loading loading-spinner"></span>
            Submitting...
          {:else}
            Submit
          {/if}
        </button>
        <button
          type="button"
          class="btn"
          on:click={() => (showModal = false)}
          disabled={submitting}
        >
          Cancel
        </button>
      </div>
    </form>
  </div>
  <label class="modal-backdrop" for="submit_modal">Close</label>
</div>

<!-- Revision Modal -->
<input
  type="checkbox"
  id="revision_modal"
  class="modal-toggle"
  bind:checked={showRevisionModal}
/>
<div class="modal" role="dialog">
  <div class="modal-box bg-base-200">
    <h3 class="font-bold text-lg mb-4">Submit Revision</h3>

    {#if revisionQuestion}
      <div class="mb-4">
        <div class="text-sm opacity-70 mb-1">Problem:</div>
        <div class="font-semibold">{revisionQuestion.problem_title}</div>
      </div>

      <form on:submit|preventDefault={handleRevisionSubmit}>
        <div class="form-control mb-4">
          <label class="label" for="revision_code_input">
            <span class=" text-sm mb-1">Your Code</span>
          </label>
          <textarea
            id="revision_code_input"
            placeholder="Paste your solution here..."
            class="textarea textarea-bordered w-full h-64"
            bind:value={revisionCode}
            disabled={submittingRevision}
            required
          ></textarea>
        </div>

        <div class="form-control mb-4">
          <fieldset>
            <legend class="label">
              <span class="text-sm mb-1">How difficult was it?</span>
            </legend>
            <div class="flex flex-col gap-2">
              {#each difficulties as d}
                <label class="label cursor-pointer justify-start gap-3">
                  <input
                    type="radio"
                    name="difficulty"
                    class={`radio radio-primary radio-xs`}
                    value={d.value}
                    bind:group={revisionDifficulty}
                    disabled={submittingRevision}
                  />
                  <span class="label-text">{d.label}</span>
                </label>
              {/each}
            </div>
          </fieldset>
        </div>

        <div class="modal-action">
          <button
            type="submit"
            class="btn btn-primary"
            disabled={submittingRevision}
          >
            {#if submittingRevision}
              <span class="loading loading-spinner"></span>
              Submitting...
            {:else}
              Submit
            {/if}
          </button>
          <button
            type="button"
            class="btn"
            on:click={() => (showRevisionModal = false)}
            disabled={submittingRevision}
          >
            Cancel
          </button>
        </div>
      </form>
    {/if}
  </div>
  <label class="modal-backdrop" for="revision_modal">Close</label>
</div>

{#snippet fab(children)}
  <div class="fab">
    <!-- Main FAB trigger: focusable for accessibility -->
    <div tabindex="0" role="button" class="btn btn-lg btn-circle btn-primary">
      F
    </div>

    <!-- Visual close (not focusable) -->
    <div class="fab-close">
      Close <span class="btn btn-circle btn-lg btn-accent">✕</span>
    </div>

    <!-- FAB actions -->
    <div>
      Logout <button
        class="btn btn-lg btn-circle btn-accent"
        on:click={handleLogout}>⎋</button
      >
    </div>
    <div>
      Submit Code <button
        class="btn btn-lg btn-circle"
        on:click={() => (showModal = true)}>+</button
      >
    </div>
    <div>Label B <button class="btn btn-lg btn-circle">B</button></div>
    <div>Label C <button class="btn btn-lg btn-circle">C</button></div>
  </div>
{/snippet}

{#snippet navbar(children)}
  <div class="flex justify-between items-center">
    <div class="font-chillax text-2xl font-bold">Swecoder</div>
    <div class="font-mono text-sm flex items-baseline gap-3">
      <span>{dateStr}</span>
      <span class="countdown">
        <span style="--value:{hour12};" aria-live="polite" aria-label="hours-12"
          >{hh}</span
        >
        :
        <span
          style="--value:{today.getMinutes()};"
          aria-live="polite"
          aria-label="minutes">{mm}</span
        >
      </span>
      <span>{ampm}</span>
    </div>
  </div>{/snippet}
