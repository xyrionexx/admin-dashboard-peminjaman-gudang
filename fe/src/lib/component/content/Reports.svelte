<script>
	import { onMount } from 'svelte';

	// Data dummy untuk demo
	let peminjaman = [
		{
			kode_pinjam: 'PJM001',
			tanggal_pinjam: '2024-08-15T08:30:00Z',
			tanggal_kembali: '2024-08-22T15:00:00Z',
			status_pinjam: 'Selesai',
			nis: 'KP-001-2023',
			nama_peminjam: 'Ahmad Rizki',
			kelas: 'XII RPL 1',
			items: [
				{ nama_barang: 'Laptop Asus X441BA', jumlah: 2, status: 'Sudah Dikembalikan' },
				{ nama_barang: 'Kalkulator Casio', jumlah: 5, status: 'Sudah Dikembalikan' }
			]
		},
		{
			kode_pinjam: 'PJM002',
			tanggal_pinjam: '2024-08-20T10:15:00Z',
			tanggal_kembali: null,
			status_pinjam: 'Masih Dipinjam',
			nis: 'KP-002-2023',
			nama_peminjam: 'Siti Nurhaliza',
			kelas: 'XI MM 2',
			items: [{ nama_barang: 'Mikroskop Olympus', jumlah: 3, status: 'Terlambat' }]
		},
		{
			kode_pinjam: 'PJM003',
			tanggal_pinjam: '2024-09-01T11:20:00Z',
			tanggal_kembali: null,
			status_pinjam: 'Masih Dipinjam',
			nis: 'KP-004-2023',
			nama_peminjam: 'Budi Santoso',
			kelas: 'X TKJ 1',
			nuptk: '196801011990031001',
			nama_guru: 'Pak Agus Wijaya, S.Pd',
			items: [
				{ nama_barang: 'Laptop Asus X441BA', jumlah: 1, status: 'Belum Dikembalikan' },
				{ nama_barang: 'Kalkulator Casio', jumlah: 10, status: 'Belum Dikembalikan' }
			]
		}
	];

	// Filter states
	let filterStatus = 'Semua';
	let filterTanggalMulai = '';
	let filterTanggalAkhir = '';
	let filterPeminjam = '';

	// Computed filtered data
	$: filteredData = peminjaman.filter((item) => {
		if (filterStatus !== 'Semua' && item.status_pinjam !== filterStatus) return false;
		if (filterTanggalMulai && new Date(item.tanggal_pinjam) < new Date(filterTanggalMulai))
			return false;
		if (filterTanggalAkhir && new Date(item.tanggal_pinjam) > new Date(filterTanggalAkhir))
			return false;
		if (filterPeminjam && !item.nama_peminjam.toLowerCase().includes(filterPeminjam.toLowerCase()))
			return false;
		return true;
	});

	// Statistics
	$: stats = {
		total: peminjaman.length,
		selesai: peminjaman.filter((p) => p.status_pinjam === 'Selesai').length,
		masihDipinjam: peminjaman.filter((p) => p.status_pinjam === 'Masih Dipinjam').length,
		terlambat: peminjaman.filter((p) => p.items.some((item) => item.status === 'Terlambat')).length
	};

	function formatDate(dateString) {
		if (!dateString) return '-';
		return new Date(dateString).toLocaleDateString('id-ID', {
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		});
	}

	function formatDateTime(dateString) {
		if (!dateString) return '-';
		return new Date(dateString).toLocaleDateString('id-ID', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	}

	function getStatusBadge(status) {
		switch (status) {
			case 'Selesai':
				return 'bg-green-100 text-green-800 border-green-200';
			case 'Masih Dipinjam':
				return 'bg-yellow-100 text-yellow-800 border-yellow-200';
			case 'Sedang Diambil':
				return 'bg-blue-100 text-blue-800 border-blue-200';
			case 'Dibatalkan':
				return 'bg-gray-100 text-gray-800 border-gray-200';
			case 'Terlambat':
				return 'bg-red-100 text-red-800 border-red-200';
			case 'Sudah Dikembalikan':
				return 'bg-green-100 text-green-800 border-green-200';
			case 'Belum Dikembalikan':
				return 'bg-orange-100 text-orange-800 border-orange-200';
			default:
				return 'bg-gray-100 text-gray-800 border-gray-200';
		}
	}

	function printReport() {
		window.print();
	}

	function exportCSV() {
		const headers = [
			'Kode Pinjam',
			'Tanggal Pinjam',
			'Tanggal Kembali',
			'Status',
			'Peminjam',
			'Kelas/Guru',
			'Barang'
		];
		const csvContent = [
			headers.join(','),
			...filteredData.map((item) =>
				[
					item.kode_pinjam,
					formatDate(item.tanggal_pinjam),
					formatDate(item.tanggal_kembali),
					item.status_pinjam,
					item.nama_peminjam,
					item.kelas || item.nama_guru || '-',
					item.items.map((i) => `${i.nama_barang} (${i.jumlah})`).join('; ')
				].join(',')
			)
		].join('\n');

		const blob = new Blob([csvContent], { type: 'text/csv' });
		const url = window.URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `laporan-peminjaman-${new Date().toISOString().split('T')[0]}.csv`;
		a.click();
	}

	let currentDate = new Date().toLocaleDateString('id-ID', {
		weekday: 'long',
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	});
</script>

<div class="min-h-screen bg-gray-50 p-6">
	<div class="mx-auto max-w-6xl">
		<!-- Header Laporan -->
		<div
			class="mb-6 rounded-lg border border-gray-200 bg-white shadow-sm print:border-gray-300 print:shadow-none"
		>
			<div class="border-b border-gray-200 bg-blue-50 px-8 py-6">
				<div class="text-center">
					<h1 class="mb-2 text-2xl font-bold text-blue-900">SMK NEGERI 1 BANDUNG</h1>
					<p class="mb-1 text-gray-700">
						Jl. Wastukancana No.3, Regol, Kota Bandung, Jawa Barat 40251
					</p>
					<p class="text-sm text-gray-600">Telp: (022) 4233802 | Email: info@smkn1bandung.sch.id</p>
				</div>
			</div>

			<div class="px-8 py-6">
				<div class="mb-4 border-b-2 border-blue-900 pb-4 text-center">
					<h2 class="text-xl font-bold uppercase text-gray-900">
						LAPORAN PEMINJAMAN BARANG GUDANG
					</h2>
					<p class="mt-2 text-gray-600">
						Periode: {formatDate(new Date())} | Total Data: {filteredData.length}
					</p>
				</div>

				<div class="flex items-center justify-between text-sm text-gray-600">
					<div>
						<p><span class="font-medium">Tanggal Cetak:</span> {currentDate}</p>
						<p><span class="font-medium">Dicetak oleh:</span> Administrator</p>
					</div>
					<div class="text-right">
						<p>
							<span class="font-medium">No. Laporan:</span> RPT/GDG/{new Date().getFullYear()}/001
						</p>
						<p><span class="font-medium">Halaman:</span> 1 dari 1</p>
					</div>
				</div>
			</div>
		</div>

		<!-- Controls (No Print) -->
		<div class="mb-6 rounded-lg border border-gray-200 bg-white shadow-sm print:hidden">
			<div class="border-b border-gray-200 px-6 py-4">
				<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
					<h3 class="text-lg font-semibold text-gray-900">Filter & Kontrol</h3>
					<div class="flex flex-wrap gap-3">
						<button
							on:click={printReport}
							class="flex items-center gap-2 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
						>
							<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
								></path>
							</svg>
							Cetak Laporan
						</button>
						<button
							on:click={exportCSV}
							class="flex items-center gap-2 rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-green-700"
						>
							<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
								></path>
							</svg>
							Export Excel
						</button>
					</div>
				</div>
			</div>

			<div class="px-6 py-4">
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
					<div>
						<label class="mb-1 block text-sm font-medium text-gray-700">Status</label>
						<select
							bind:value={filterStatus}
							class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
						>
							<option value="Semua">Semua Status</option>
							<option value="Selesai">Selesai</option>
							<option value="Masih Dipinjam">Masih Dipinjam</option>
							<option value="Sedang Diambil">Sedang Diambil</option>
						</select>
					</div>

					<div>
						<label class="mb-1 block text-sm font-medium text-gray-700">Tanggal Mulai</label>
						<input
							type="date"
							bind:value={filterTanggalMulai}
							class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
						/>
					</div>

					<div>
						<label class="mb-1 block text-sm font-medium text-gray-700">Tanggal Akhir</label>
						<input
							type="date"
							bind:value={filterTanggalAkhir}
							class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
						/>
					</div>

					<div>
						<label class="mb-1 block text-sm font-medium text-gray-700">Cari Peminjam</label>
						<input
							type="text"
							placeholder="Nama peminjam..."
							bind:value={filterPeminjam}
							class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
						/>
					</div>
				</div>
			</div>
		</div>

		<!-- Ringkasan Statistik -->
		<div class="mb-6 rounded-lg border border-gray-200 bg-white shadow-sm">
			<div class="border-b border-gray-200 bg-blue-50 px-6 py-4">
				<h3 class="text-lg font-semibold text-blue-900">Ringkasan Data</h3>
			</div>
			<div class="p-6">
				<div class="grid grid-cols-2 gap-6 sm:grid-cols-4">
					<div class="text-center">
						<div class="mb-1 text-3xl font-bold text-blue-600">{stats.total}</div>
						<div class="text-sm font-medium text-gray-600">Total Peminjaman</div>
					</div>
					<div class="text-center">
						<div class="mb-1 text-3xl font-bold text-green-600">{stats.selesai}</div>
						<div class="text-sm font-medium text-gray-600">Selesai</div>
					</div>
					<div class="text-center">
						<div class="mb-1 text-3xl font-bold text-yellow-600">{stats.masihDipinjam}</div>
						<div class="text-sm font-medium text-gray-600">Masih Dipinjam</div>
					</div>
					<div class="text-center">
						<div class="mb-1 text-3xl font-bold text-red-600">{stats.terlambat}</div>
						<div class="text-sm font-medium text-gray-600">Terlambat</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Tabel Data -->
		<div class="rounded-lg border border-gray-200 bg-white shadow-sm">
			<div class="border-b border-gray-200 bg-blue-50 px-6 py-4">
				<h3 class="text-lg font-semibold text-blue-900">Data Peminjaman Barang</h3>
			</div>

			<div class="overflow-x-auto">
				<table class="w-full">
					<thead class="border-b border-gray-200 bg-gray-50">
						<tr>
							<th
								class="border-r border-gray-200 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-700"
								>No</th
							>
							<th
								class="border-r border-gray-200 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-700"
								>Kode Pinjam</th
							>
							<th
								class="border-r border-gray-200 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-700"
								>Peminjam</th
							>
							<th
								class="border-r border-gray-200 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-700"
								>Tanggal Pinjam</th
							>
							<th
								class="border-r border-gray-200 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-700"
								>Barang Dipinjam</th
							>
							<th
								class="border-r border-gray-200 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-700"
								>Status</th
							>
							<th
								class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-700"
								>Tanggal Kembali</th
							>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200 bg-white">
						{#each filteredData as item, index}
							<tr class="hover:bg-gray-50 print:hover:bg-transparent">
								<td
									class="whitespace-nowrap border-r border-gray-200 px-4 py-4 text-sm font-medium text-gray-900"
								>
									{index + 1}
								</td>
								<td
									class="whitespace-nowrap border-r border-gray-200 px-4 py-4 text-sm font-medium text-blue-600"
								>
									{item.kode_pinjam}
								</td>
								<td class="border-r border-gray-200 px-4 py-4">
									<div class="text-sm font-medium text-gray-900">{item.nama_peminjam}</div>
									<div class="text-xs text-gray-500">{item.kelas || item.nama_guru || '-'}</div>
									<div class="text-xs text-gray-400">{item.nis}</div>
								</td>
								<td
									class="whitespace-nowrap border-r border-gray-200 px-4 py-4 text-sm text-gray-900"
								>
									{formatDate(item.tanggal_pinjam)}
								</td>
								<td class="border-r border-gray-200 px-4 py-4">
									<div class="space-y-1">
										{#each item.items as barang}
											<div class="text-sm">
												<span class="font-medium text-gray-900">{barang.nama_barang}</span>
												<span class="ml-2 text-gray-500">({barang.jumlah} unit)</span>
												<span
													class="ml-2 inline-block rounded-full border px-2 py-0.5 text-xs {getStatusBadge(
														barang.status
													)}"
												>
													{barang.status}
												</span>
											</div>
										{/each}
									</div>
								</td>
								<td class="whitespace-nowrap border-r border-gray-200 px-4 py-4">
									<span
										class="inline-block rounded-full border px-3 py-1 text-xs font-medium {getStatusBadge(
											item.status_pinjam
										)}"
									>
										{item.status_pinjam}
									</span>
								</td>
								<td class="whitespace-nowrap px-4 py-4 text-sm text-gray-900">
									{formatDate(item.tanggal_kembali)}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			{#if filteredData.length === 0}
				<div class="py-12 text-center">
					<svg
						class="mx-auto h-12 w-12 text-gray-400"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
						></path>
					</svg>
					<h3 class="mt-2 text-sm font-medium text-gray-900">Tidak ada data ditemukan</h3>
					<p class="mt-1 text-sm text-gray-500">Silakan ubah filter untuk menampilkan data.</p>
				</div>
			{/if}
		</div>

		<!-- Footer Laporan -->
		<div class="mt-6 rounded-lg border border-gray-200 bg-white shadow-sm">
			<div class="px-8 py-6">
				<div class="flex items-end justify-between">
					<div class="text-sm text-gray-600">
						<p class="mb-1 font-medium">Keterangan:</p>
						<ul class="space-y-1 text-xs">
							<li>• Laporan ini dibuat secara otomatis oleh sistem</li>
							<li>• Data yang ditampilkan adalah data real-time</li>
							<li>• Untuk informasi lebih lanjut hubungi bagian gudang</li>
						</ul>
					</div>

					<div class="text-center">
						<p class="mb-8 text-sm text-gray-700">Bandung, {formatDate(new Date())}</p>
						<div class="mb-2 w-48 border-b border-gray-400"></div>
						<p class="text-sm font-medium text-gray-900">Kepala Bagian Gudang</p>
						<p class="mt-1 text-xs text-gray-600">NIP. 196801011990031001</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	@media print {
		@page {
			margin: 1.5cm;
			size: A4;
		}

		body {
			background: white !important;
			-webkit-print-color-adjust: exact;
			print-color-adjust: exact;
		}

		.print\\:hidden {
			display: none !important;
		}

		.print\\:shadow-none {
			box-shadow: none !important;
		}

		.print\\:border-gray-300 {
			border-color: #d1d5db !important;
		}

		.print\\:hover\\:bg-transparent:hover {
			background-color: transparent !important;
		}

		/* Ensure table borders are visible in print */
		table,
		th,
		td {
			border-collapse: collapse;
		}

		th,
		td {
			border: 1px solid #d1d5db !important;
		}
	}

	/* Responsive table */
	@media (max-width: 768px) {
		table {
			font-size: 12px;
		}

		.px-4 {
			padding-left: 0.5rem;
			padding-right: 0.5rem;
		}
	}
</style>
