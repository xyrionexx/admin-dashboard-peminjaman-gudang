<script lang="ts">
	import Sidebar from '$lib/component/sidebars.svelte';
	import Dashboard from '$lib/component/content/dashboard.svelte';
	import Analytics from '$lib/component/content/Analytics.svelte';
	import Users from '$lib/component/content/Users.svelte';
	import Products from '$lib/component/content/Products.svelte';
	import Barang from '$lib/component/content/barang.svelte';
	import Reports from '$lib/component/content/Reports.svelte';
	import Settings from '$lib/component/content/Settings.svelte';
	import type { Component } from 'svelte';

	let sidebarCollapsed: boolean = $state(false);
	let mobileMenuOpen: boolean = $state(false);
	let activePage: string = $state('Dashboard');

	const pageComponents: Record<string, Component<any>> = {
		Dashboard,
		Analytics,
		Users,
		Products,
		Barang,
		Reports,
		Settings
	};

	function toggleSidebar(): void {
		sidebarCollapsed = !sidebarCollapsed;
	}

	function toggleMobileMenu(): void {
		mobileMenuOpen = !mobileMenuOpen;
	}

	function closeMobileMenu(): void {
		mobileMenuOpen = false;
	}

	function handlePageChange(pageName: string): void {
		activePage = pageName;
		closeMobileMenu();
	}

	let SvelteComponent: Component<any> = $derived(pageComponents[activePage]);
</script>

<div class="flex h-screen bg-gray-50">
	<!-- Mobile overlay -->
	{#if mobileMenuOpen}
		<div
			class="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
			role="button"
			tabindex="0"
			aria-label="Close mobile menu"
			onclick={closeMobileMenu}
			onkeydown={(event) => {
				if (event.key === 'Enter' || event.key === ' ') {
					closeMobileMenu();
				}
			}}
		></div>
	{/if}

	<!-- Sidebar -->
	<Sidebar
		collapsed={sidebarCollapsed}
		mobileOpen={mobileMenuOpen}
		{activePage}
		onToggle={toggleSidebar}
		onCloseMobile={closeMobileMenu}
		onPageChange={handlePageChange}
	/>

	<!-- Main content -->
	<div class="flex flex-1 flex-col overflow-hidden">
		<!-- Mobile header -->
		<header class="border-b bg-white px-4 py-3 shadow-sm lg:hidden">
			<div class="flex items-center justify-between">
				<h1 class="text-xl font-semibold text-gray-800">{activePage}</h1>
				<button
					type="button"
					onclick={toggleMobileMenu}
					class="rounded-md p-2 text-gray-600 hover:bg-gray-100"
					aria-label="Toggle mobile menu"
				>
					<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M4 6h16M4 12h16M4 18h16"
						></path>
					</svg>
				</button>
			</div>
		</header>

		<!-- Dynamic component rendering based on active page -->
		<main class="flex-1 overflow-auto p-6">
			{#if SvelteComponent}
				<SvelteComponent />
			{/if}
		</main>
	</div>
</div>
