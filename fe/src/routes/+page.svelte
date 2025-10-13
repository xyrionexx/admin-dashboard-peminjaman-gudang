<script lang="ts">
	import Sidebar from '$lib/component/sidebars.svelte';
	import Aktivitas from '$lib/component/content/dashboard.svelte';
	import Analisis from '$lib/component/content/Analytics.svelte';
	import Pengguna from '$lib/component/content/user.svelte';
	import Barang from '$lib/component/content/barang.svelte';
	import Laporan from '$lib/component/content/Reports.svelte';
	import Pengaturan from '$lib/component/content/Settings.svelte';
	import TambahBarang from '$lib/tambah/tambahbarang.svelte';
	import TambahUser from '$lib/tambah/tambahUser.svelte';
	import Update from '../update/update.svelte';
	import Detail from '$lib/component/content/detail.svelte';
	import DetailDashboard from '$lib/detailStatus/detailDashboard.svelte';
	import Scanqr from '$lib/component/content/scanqr.svelte';
	import DetailPeminjaman from '$lib/detailStatus/detailPeminjaman.svelte';
	import ScanPengembalian from '$lib/component/content/scanpengembalian.svelte';
	import UpdateUser from '../update/updateuser.svelte';

	// Get user data from the server using runes syntax
	const { data } = $props();

	import type { Component } from 'svelte';

	let sidebarCollapsed: boolean = $state(false);
	let mobileMenuOpen: boolean = $state(false);
	let activePage: string = $state('Aktivitas');

	const pageComponents: Record<string, Component<any>> = {
		Aktivitas,
		Analisis,
		Pengguna,
		Barang,
		Laporan,
		Pengaturan,
		TambahBarang,
		TambahUser,
		Update,
		Detail,
		DetailDashboard,
		Scanqr,
		ScanPengembalian,
		DetailPeminjaman,
		UpdateUser
	};
	let selectedBarangId = $state<undefined | string>(undefined);
	let selectedKategori = $state<undefined | string>(undefined);
	const SelectedComponent = $derived<Component<any>>(pageComponents[activePage]);

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
		<!-- Desktop header -->
		<header class="border-b bg-white px-6 py-3 shadow-sm hidden lg:block">
			<div class="flex items-center justify-between">
				<h1 class="text-xl font-semibold text-gray-800">{activePage}</h1>
				<div class="flex items-center space-x-4">
					{#if data.user}
					<div class="text-sm text-gray-600">Login sebagai: <span class="font-semibold">{data.user.username}</span></div>
					<a 
						href="/logout" 
						class="inline-flex items-center px-3 py-2 text-sm font-medium leading-4 text-white bg-red-600 hover:bg-red-700 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
					>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
						</svg>
						Logout
					</a>
					{/if}
				</div>
			</div>
		</header>

		<!-- Mobile header -->
		<header class="border-b bg-white px-4 py-3 shadow-sm lg:hidden">
			<div class="flex items-center justify-between">
				<h1 class="text-xl font-semibold text-gray-800">{activePage}</h1>
				<div class="flex items-center space-x-2">
					{#if data.user}
					<a 
						href="/logout" 
						aria-label="Logout"
						class="inline-flex items-center p-1 text-sm font-medium leading-4 text-white bg-red-600 hover:bg-red-700 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
					>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
						</svg>
						<span class="sr-only">Logout</span>
					</a>
					{/if}
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
			</div>
		</header>

		<!-- Dynamic component rendering -->
		<main class="flex-1 overflow-auto p-6">
			<SelectedComponent
				{...activePage === 'Update' ||
				activePage === 'DetailDashboard' ||
				activePage === 'DetailPeminjaman' ||
				activePage === 'UpdateUser'
					? { id: selectedBarangId, kategori: selectedKategori }
					: {}}
				on:pageChange={(e: CustomEvent<{ page: string; id?: string; kategori?: string }>) => {
					activePage = e.detail.page;
					selectedBarangId = e.detail.id;
					selectedKategori = e.detail.kategori;
				}}
			/>
		</main>
	</div>
</div>
