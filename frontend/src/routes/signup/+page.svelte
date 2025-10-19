<script>
  import { signup } from "$lib/auth.js";
  import { goto } from "$app/navigation";

  let username = "";
  let password = "";
  let name = "";
  let loading = false;
  let errorMessage = "";

  async function handleSubmit(event) {
    event.preventDefault();
    errorMessage = "";
    loading = true;
    try {
      const result = await signup(username, password, name || undefined);
      if (result?.ok) {
        goto("/dashboard");
      } else {
        errorMessage = "Signup failed";
      }
    } catch (e) {
      errorMessage = "Signup failed";
    } finally {
      loading = false;
    }
  }
</script>

<div class="h-[93svh] w-full flex flex-col items-center justify-center">
  <div class="font-chillax text-4xl font-bold">Swecoder</div>
  <div class="mb-5 opacity-70">Create your account</div>
  <form onsubmit={handleSubmit} class="flex flex-col gap-4 max-w-md w-full">
    <input
      type="text"
      placeholder="Username"
      class="input input-bordered w-full"
      bind:value={username}
    />
    <input
      type="text"
      placeholder="Name (optional)"
      class="input input-bordered w-full"
      bind:value={name}
    />
    <input
      type="password"
      placeholder="Password"
      class="input input-bordered w-full"
      bind:value={password}
    />
    {#if errorMessage}
      <div class="text-error text-sm">{errorMessage}</div>
    {/if}
    <button type="submit" class="btn btn-primary" disabled={loading}>
      {#if loading}Signing up...{/if}
      {#if !loading}Sign Up{/if}
    </button>
  </form>
  <div class="mt-3 text-sm text-center">
    <span class="opacity-70">Already have an account?</span>
    <a href="/login" class="link link-primary ml-1">Log in</a>
  </div>
</div>
