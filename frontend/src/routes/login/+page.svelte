<script>
  import { login } from "$lib/auth.js";
  import { goto } from "$app/navigation";

  let username = "";
  let password = "";
  let loading = false;
  let errorMessage = "";

  async function handleSubmit(event) {
    event.preventDefault();
    errorMessage = "";
    loading = true;
    try {
      const result = await login(username, password);
      if (result?.ok) {
        goto("/dashboard");
      } else {
        errorMessage =
          result?.status === 401
            ? "Wrong password"
            : result?.error || "Login failed";
        setTimeout(() => {
          errorMessage = "";
        }, 3000);
      }
    } catch (e) {
      errorMessage = "Login failed";
      setTimeout(() => {
        errorMessage = "";
      }, 3000);
    } finally {
      loading = false;
    }
  }
</script>

<div class="h-[93svh] w-full flex flex-col items-center justify-center">
  <div class="font-chillax text-4xl font-bold">Swecoder</div>
  <div class="mb-5 opacity-70">what ra sudeep where you went off</div>
  <form onsubmit={handleSubmit} class="flex flex-col gap-4 max-w-md w-full">
    <input
      type="text"
      placeholder="Username"
      class="input input-bordered w-full"
      bind:value={username}
    />
    <input
      type="password"
      placeholder="Password"
      class="input input-bordered w-full"
      bind:value={password}
    />
    <button type="submit" class="btn btn-primary">Login</button>
  </form>
  {#if errorMessage}
    <div class="toast toast-end">
      <div class="alert bg-primary text-primary-content">
        <span>{errorMessage}</span>
      </div>
    </div>
  {/if}
  <div class="mt-3 text-sm text-center">
    <span class="opacity-70">Don't have an account?</span>
    <a href="/signup" class="link link-primary ml-1">Sign up</a>
  </div>
</div>

<style>
  .font-chillax {
    font-family: "Chillax", sans-serif;
  }
</style>
