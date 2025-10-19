<script>
  import "../app.css";
  import favicon from "$lib/assets/favicon.svg";

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<div class="max-w-screen-lg mx-auto p-4 h-svh">
  {@render children?.()}
</div>
