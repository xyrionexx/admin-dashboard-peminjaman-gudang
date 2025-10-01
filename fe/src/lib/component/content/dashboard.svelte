<script lang="ts">
	import * as Pagination from '$lib/components/ui/pagination/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import BadgeCheckIcon from '@lucide/svelte/icons/badge-check';
	import { onMount, createEventDispatcher } from 'svelte';
	import QrCode from './data/qrcode.svelte';
	const dispatch = createEventDispatcher<{ pageChange: { page: string; id?: number } }>();

	interface Peminjaman {
		kode_pinjam: string;
		nis: string;
		nuptk: string;
		id_pegawai: string;
		tanggal_pinjam: string;
		tanggal_kembali: string;
		status_pinjam: 'Sedang Diambil' | 'Masih Dipinjam' | 'Dibatalkan' | 'Selesai';
	}

	let peminjaman: any[] = $state([]);
	let barang: any = {};
	let totalStok = 0;
	let totalBarang = $state(0);
	let totalPeminjaman = $state(0);

	onMount(async () => {
		try {
			const [resPeminjaman, resSummary] = await Promise.all([
				fetch('https://api.borrowfy.site/api/peminjaman/'),
				fetch('https://api.borrowfy.site/api/barang/summary')
			]);
			if (!resPeminjaman.ok || !resSummary.ok) {
				throw new Error('Gagal ambil data');
			}
			peminjaman = await resPeminjaman.json();
			barang = await resSummary.json();
			totalStok = barang.total_stok;
			totalBarang = barang.total_barang;
			totalPeminjaman = peminjaman.length;
			console.log(peminjaman);
		} catch (err) {
			console.log(err);
		}
	});

	let searchTerm = $state<string>('');

	let filteredUsers = $derived(
		peminjaman.filter(
			(user) =>
				user.nis.toLowerCase().includes(searchTerm.toLowerCase()) ||
				user.kode_pinjam.toLowerCase().includes(searchTerm.toLowerCase())
		)
	);

	const totalData = $derived(() => filteredUsers.length);

	function getStatusColor(
		status: 'Sedang Diambil' | 'Masih Dipinjam' | 'Dibatalkan' | 'Selesai'
	): string {
		switch (status) {
			case 'Sedang Diambil':
				return 'bg-yellow-100 text-yellow-700';
			case 'Masih Dipinjam':
				return 'bg-blue-100 text-blue-700';
			case 'Selesai':
				return 'bg-green-100 text-green-700';
			case 'Dibatalkan':
				return 'bg-red-100 text-red-700';
			default:
				return 'bg-gray-100 text-gray-700';
		}
	}

	function getStatusText(
		status: 'Sedang Diambil' | 'Masih Dipinjam' | 'Dibatalkan' | 'Selesai'
	): string {
		switch (status) {
			case 'Sedang Diambil':
				return 'Dipinjam';
			case 'Masih Dipinjam':
				return 'Aktid';
			case 'Selesai':
				return 'Selesai';
			case 'Dibatalkan':
				return 'Dibatalkan';
			default:
				return 'Uknown';
		}
	}

	let perPage = 10;
	let currentPage = $state(1);

	const paginatedUser = $derived(() => {
		const start = (currentPage - 1) * perPage;
		const end = start + perPage;
		return filteredUsers.slice(start, end);
	});

	function formatDate(dateString: string) {
		if (!dateString) return '-';

		const date = new Date(dateString);
		const dateOptions: Intl.DateTimeFormatOptions = {
			day: 'numeric',
			month: 'short',
			year: 'numeric'
		};

		const timeOptions: Intl.DateTimeFormatOptions = {
			hour: '2-digit',
			minute: '2-digit',
			second: '2-digit',
			hour12: false
		};

		const datePart = new Intl.DateTimeFormat('id-ID', dateOptions).format(date);
		const timePart = new Intl.DateTimeFormat('id-ID', timeOptions).format(date);

		return `${datePart} ${timePart}`;
	}
</script>

<div class="min-h-screen bg-gray-50 p-6">
	<div class="mx-auto max-w-6xl">
		<!-- Header -->
		<div class="mb-8">
			<h1 class="mb-2 text-3xl font-bold text-gray-800">Dashboard Peminjaman Barang</h1>
			<p class="text-gray-600">Kelola peminjaman barang sekolah dengan mudah</p>
		</div>

		<!-- Stats Cards -->
		<div class="mb-8 grid grid-cols-1 gap-6 md:grid-cols-3">
			<div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
				<div class="flex items-center">
					<div class="rounded-lg bg-blue-50 p-3">
						<svg
							class="h-6 w-6 text-blue-600"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
							/>
						</svg>
					</div>
					<div class="ml-4">
						<p class="text-sm font-medium text-gray-600">Total Barang</p>
						<p class="text-2xl font-bold text-gray-900">{totalBarang}</p>
					</div>
				</div>
			</div>

			<div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
				<div class="flex items-center">
					<div class="rounded-lg bg-blue-50 p-3">
						<svg
							class="h-6 w-6 text-blue-600"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
							/>
						</svg>
					</div>
					<div class="ml-4">
						<p class="text-sm font-medium text-gray-600">Sedang Dipinjam</p>
						<p class="text-2xl font-bold text-gray-900">{totalPeminjaman}</p>
					</div>
				</div>
			</div>

			<div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
				<div class="flex items-center">
					<div class="rounded-lg bg-blue-50 p-3">
						<svg
							class="h-6 w-6 text-blue-600"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
							/>
						</svg>
					</div>
					<div class="ml-4">
						<p class="text-sm font-medium text-gray-600">Terlambat</p>
						<p class="text-2xl font-bold text-gray-900">7</p>
					</div>
				</div>
			</div>
		</div>

		<!-- Search and Table -->
		<div class="rounded-lg border border-gray-200 bg-white shadow-sm">
			<div class="border-b border-gray-200 p-6">
				<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
					<h2 class="text-lg font-semibold text-gray-800">Daftar Peminjaman</h2>
					<div class="relative">
						<input
							type="text"
							placeholder="Cari nama atau kelas..."
							bind:value={searchTerm}
							class="w-full rounded-lg border border-gray-300 py-2 pl-10 pr-4 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 sm:w-64"
						/>
						<svg
							class="absolute left-3 top-2.5 h-5 w-5 text-gray-400"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
							/>
						</svg>
					</div>
				</div>
			</div>

			<div class="overflow-x-auto">
				<table class="w-full">
					<thead class="bg-gray-50">
						<tr>
							<th
								class="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Kode Pinjam</th
							>
							<th
								class="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>NIS</th
							>
							<th
								class="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>NUPTK</th
							>
							<th
								class="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>id_pegawai</th
							>
							<th
								class="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Tanggal Pinjam</th
							>
							<th
								class="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Tanggal Kembali</th
							>
							<th
								class="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Status Pinjam</th
							>
							<th
								class="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Lihat Data</th
							>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200 bg-white">
						{#each paginatedUser() as user}
							<tr class="transition-colors hover:bg-gray-50">
								<td class="whitespace-nowrap px-5 py-4">
									<div class="text-sm font-medium text-gray-900">{user.kode_pinjam}</div>
								</td>
								<td class="whitespace-nowrap px-5 py-4">
									<div class="text-sm text-gray-600">{user.nis}</div>
								</td>
								<td class="whitespace-nowrap px-5 py-4">
									<div class="text-sm text-gray-600">{user.nuptk}</div>
								</td>
								<td class="whitespace-nowrap px-5 py-4">
									<div class="text-sm text-gray-600">{user.id_pegawai}</div>
								</td>
								<td class="whitespace-nowrap px-5 py-4">
									<div class="text-sm text-gray-600">{formatDate(user.tanggal_pinjam)}</div>
								</td>
								<td class="whitespace-nowrap px-5 py-4">
									<div class="text-sm text-gray-600">{formatDate(user.tanggal_kembali)}</div>
								</td>
								<td class="rounded-4xl whitespace-nowrappy-4">
									<div>
										<Badge class={`${getStatusColor(user.status_pinjam)} rounded-2xl`}>
											{user.status_pinjam}
										</Badge>
									</div>
								</td>
								<td>
									<button
										onclick={() =>
											dispatch('pageChange', { page: 'DetailDashboard', id: user.kode_pinjam })}
										>Lihat Data</button
									></td
								>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<!-- Pagination -->
			<div class="border-t border-gray-200 px-6 py-4">
				<Pagination.Root count={totalData()} {perPage} bind:page={currentPage}>
					{#snippet children({ pages, currentPage })}
						<Pagination.Content>
							<Pagination.Item>
								<Pagination.PrevButton />
							</Pagination.Item>
							{#each pages as page (page.key)}
								{#if page.type === 'ellipsis'}
									<Pagination.Item>
										<Pagination.Ellipsis />
									</Pagination.Item>
								{:else}
									<Pagination.Item>
										<Pagination.Link {page} isActive={currentPage === page.value}>
											{page.value}
										</Pagination.Link>
									</Pagination.Item>
								{/if}
							{/each}
							<Pagination.Item>
								<Pagination.NextButton />
							</Pagination.Item>
						</Pagination.Content>
					{/snippet}
				</Pagination.Root>
			</div>
		</div>
	</div>
</div>
