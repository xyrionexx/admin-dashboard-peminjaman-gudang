<script lang="ts">
	import { onMount } from 'svelte';
	import { format } from 'date-fns';
	import { id } from 'date-fns/locale';

	interface DetailPeminjaman {
		kode_detail: string;
		kode_pinjam: string;
		nama_peminjam: string;
		jenis_peminjam: string;
		nama_barang: string;
		jumlah_dipinjam: number;
		status_barang: string;
		tanggal_pinjam: string;
		tanggal_kembali: string;
		batas_ambil_val: string;
		status_peminjaman: string;
	}

	let detailPeminjaman: DetailPeminjaman[] = [];
	let isLoading = true;
	let error: string | null = null;
	let filterStatus = 'all';
	let searchQuery = '';
	let startDate = '';
	let endDate = '';

	const formatDate = (dateString: string): string => {
		try {
			const date = new Date(dateString);
			return format(date, 'dd MMMM yyyy, HH:mm', { locale: id });
		} catch (error) {
			return dateString;
		}
	};

	const printReport = () => {
		window.print();
	};

	const getStatusClass = (status: string): string => {
		switch (status) {
			case 'Selesai':
				return 'bg-green-100 text-green-800';
			case 'Masih Dipinjam':
				return 'bg-blue-100 text-blue-800';
			case 'Terlambat':
				return 'bg-red-100 text-red-800';
			default:
				return 'bg-gray-100 text-gray-800';
		}
	};

	onMount(async () => {
		console.log('Component mounted, fetching data...');
		try {
			// The correct endpoint based on urls.py
			const apiUrl = 'http://127.0.0.1:8000/api/detail/peminjaman/list';
			console.log('Fetching from:', apiUrl);

			const response = await fetch(apiUrl);
			console.log('Response status:', response.status);

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const responseText = await response.text();
			console.log('Raw response:', responseText);

			if (responseText) {
				try {
					detailPeminjaman = JSON.parse(responseText);
					console.log('Parsed data:', detailPeminjaman);
					isLoading = false;
				} catch (parseError) {
					console.error('JSON parse error:', parseError);
					error = 'Failed to parse server response';
					isLoading = false;
				}
			} else {
				console.log('Empty response received');
				detailPeminjaman = [];
				isLoading = false;
			}
		} catch (e: unknown) {
			console.error('Error fetching data:', e);
			error = e instanceof Error ? e.message : String(e);
			isLoading = false;

			// Fallback to the other possible endpoint
			try {
				console.log('Trying fallback endpoint...');
				const fallbackUrl = 'http://127.0.0.1:8000/api/detail/peminjaman/list';
				const fallbackResponse = await fetch(fallbackUrl);

				if (fallbackResponse.ok) {
					console.log('Fallback succeeded');
					const data = await fallbackResponse.json();
					detailPeminjaman = data;
					error = null;
					isLoading = false;
					console.log('Fallback data:', detailPeminjaman);
				}
			} catch (fallbackError) {
				console.error('Fallback also failed:', fallbackError);
			}
		}
	});

	// Reactive statement untuk filtering - akan otomatis update ketika dependencies berubah
	$: filteredData = (() => {
		console.log('Filtering data:', {
			totalData: detailPeminjaman.length,
			filterStatus,
			searchQuery,
			startDate,
			endDate
		});

		if (detailPeminjaman.length === 0) {
			return [];
		}

		let filtered = [...detailPeminjaman];

		// Filter by status
		if (filterStatus !== 'all') {
			filtered = filtered.filter((item) => item.status_peminjaman === filterStatus);
			console.log(`After status filter (${filterStatus}):`, filtered.length);
		}

		// Filter by search query (across multiple fields)
		if (searchQuery.trim()) {
			const query = searchQuery.toLowerCase().trim();
			filtered = filtered.filter(
				(item) =>
					item.kode_detail.toLowerCase().includes(query) ||
					item.kode_pinjam.toLowerCase().includes(query) ||
					item.nama_peminjam.toLowerCase().includes(query) ||
					item.nama_barang.toLowerCase().includes(query)
			);
			console.log(`After search filter (${query}):`, filtered.length);
		}

		// Filter by date range
		if (startDate && endDate) {
			const start = new Date(startDate);
			const end = new Date(endDate);
			end.setHours(23, 59, 59, 999); // Include the end date fully

			filtered = filtered.filter((item) => {
				try {
					const pinjamDate = new Date(item.tanggal_pinjam);
					const isInRange = pinjamDate >= start && pinjamDate <= end;
					return isInRange;
				} catch (dateError) {
					console.warn('Invalid date format:', item.tanggal_pinjam);
					return false;
				}
			});
			console.log(`After date filter (${startDate} to ${endDate}):`, filtered.length);
		}

		console.log('Final filtered data:', filtered.length);
		return filtered;
	})();
</script>

<svelte:head>
	<style>
		@media print {
			.no-print {
				display: none !important;
			}
			.print-only {
				display: block !important;
			}
			body {
				padding: 0;
				margin: 0;
			}
			table {
				width: 100%;
				border-collapse: collapse;
			}
			th,
			td {
				border: 1px solid #ddd;
				padding: 8px;
				text-align: left;
			}
			.page-header {
				position: fixed;
				top: 0;
				width: 100%;
				text-align: center;
				margin-bottom: 20px;
			}
			.page-footer {
				position: fixed;
				bottom: 0;
				width: 100%;
				text-align: center;
				margin-top: 20px;
			}
		}
		.print-only {
			display: none;
		}
	</style>
</svelte:head>

<div class="p-4">
	<!-- Header -->
	<div class="mb-6 flex items-center justify-between">
		<h1 class="text-4xl font-semibold">Laporan Peminjaman Barang</h1>
		<button
			on:click={printReport}
			class="no-print flex items-center rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="mr-2 h-5 w-5"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2z"
				/>
			</svg>
			Cetak Laporan
		</button>
	</div>

	<!-- Print Header (Only shows when printing) -->
	<div class="print-only page-header">
		<h1 class="mb-2 text-2xl font-bold">LAPORAN PEMINJAMAN BARANG</h1>
		<p>Tanggal Cetak: {formatDate(new Date().toISOString())}</p>
		<hr class="my-4" />
	</div>

	<!-- Filters -->
	<div class="no-print mb-6 rounded-lg bg-white p-4 shadow">
		<div class="grid grid-cols-1 gap-4 md:grid-cols-4">
			<div>
				<label for="statusFilter" class="block text-sm font-medium text-gray-700"
					>Status Peminjaman</label
				>
				<select
					id="statusFilter"
					bind:value={filterStatus}
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				>
					<option value="all">Semua Status</option>
					<option value="Selesai">Selesai</option>
					<option value="Masih Dipinjam">Masih Dipinjam</option>
					<option value="Terlambat">Terlambat</option>
				</select>
			</div>

			<div>
				<label for="searchQuery" class="block text-sm font-medium text-gray-700">Cari</label>
				<input
					type="text"
					id="searchQuery"
					bind:value={searchQuery}
					placeholder="Kode, nama peminjam, barang..."
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				/>
			</div>

			<div>
				<label for="startDate" class="block text-sm font-medium text-gray-700">Tanggal Mulai</label>
				<input
					type="date"
					id="startDate"
					bind:value={startDate}
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				/>
			</div>

			<div>
				<label for="endDate" class="block text-sm font-medium text-gray-700">Tanggal Akhir</label>
				<input
					type="date"
					id="endDate"
					bind:value={endDate}
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
				/>
			</div>
		</div>
	</div>

	<!-- Loading State -->
	{#if isLoading}
		<div class="flex h-64 items-center justify-center">
			<div class="h-12 w-12 animate-spin rounded-full border-b-2 border-t-2 border-blue-500"></div>
		</div>
	{:else if error}
		<div class="mb-4 rounded border border-red-400 bg-red-100 px-4 py-3 text-red-700">
			<p><strong>Error:</strong> {error}</p>
			<p>Gagal mengambil data dari server. Silahkan coba lagi nanti.</p>
		</div>
	{:else}
		<!-- Report Summary -->
		<div class="mb-6 rounded-lg bg-white p-4 shadow">
			<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
				<div class="rounded-md border border-blue-200 bg-blue-50 p-4">
					<p class="text-lg font-medium">Total Peminjaman</p>
					<p class="text-3xl font-bold">{filteredData.length}</p>
				</div>
				<div class="rounded-md border border-green-200 bg-green-50 p-4">
					<p class="text-lg font-medium">Selesai</p>
					<p class="text-3xl font-bold">
						{filteredData.filter((item) => item.status_peminjaman === 'Selesai').length}
					</p>
				</div>
				<div class="rounded-md border border-amber-200 bg-amber-50 p-4">
					<p class="text-lg font-medium">Dalam Proses</p>
					<p class="text-3xl font-bold">
						{filteredData.filter((item) => item.status_peminjaman === 'Masih Dipinjam').length}
					</p>
				</div>
			</div>
		</div>

		<!-- Report Table -->
		<div class="overflow-x-auto rounded-lg bg-white shadow">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gray-50">
					<tr>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Kode Detail</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Kode Pinjam</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Peminjam</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Jenis</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Barang</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Jumlah</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Status Barang</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Tanggal Pinjam</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Tanggal Kembali</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Status</th
						>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 bg-white">
					{#each filteredData as item, i}
						<tr class={i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
							<td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">
								{item.kode_detail}
							</td>
							<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
								{item.kode_pinjam}
							</td>
							<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
								{item.nama_peminjam}
							</td>
							<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
								{item.jenis_peminjam}
							</td>
							<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
								{item.nama_barang}
							</td>
							<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
								{item.jumlah_dipinjam}
							</td>
							<td class="whitespace-nowrap px-6 py-4 text-sm">
								<span
									class={item.status_barang === 'Sudah Dikembalikan'
										? 'rounded-full bg-green-100 px-2 py-1 text-xs text-green-800'
										: 'rounded-full bg-yellow-100 px-2 py-1 text-xs text-yellow-800'}
								>
									{item.status_barang}
								</span>
							</td>
							<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
								{formatDate(item.tanggal_pinjam)}
							</td>
							<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
								{formatDate(item.tanggal_kembali)}
							</td>
							<td class="whitespace-nowrap px-6 py-4">
								<span
									class={`rounded-full px-2 py-1 text-xs ${getStatusClass(item.status_peminjaman)}`}
								>
									{item.status_peminjaman}
								</span>
							</td>
						</tr>
					{:else}
						<tr>
							<td colspan="10" class="px-6 py-10 text-center text-gray-500">
								Tidak ada data yang ditemukan
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>

		<!-- Print Footer (Only shows when printing) -->
		<div class="print-only page-footer">
			<hr class="my-4" />
			<p>{new Date().getFullYear()} Admin Dashboard Peminjaman Gudang</p>
			<p>Halaman 1</p>
		</div>
	{/if}
</div>
