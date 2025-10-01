<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import Qrcode from '$lib/component/content/data/qrcode.svelte';
	const dispatch = createEventDispatcher<{ pageChange: { page: string; id?: number } }>();

	const props = $props<{ id: string }>(); // simpan props reaktif
	let peminjaman: any = $state(null);

	async function fetchData() {
		if (!props.id) {
			console.log('❌ id kosong');
			return;
		}

		console.log('🔍 Fetch dengan id:', props.id);

		try {
			const res = await fetch(`https://api.borrowfy.site/api/detailpeminjaman/${props.id}/`);
			console.log('📡 Status response:', res.status);

			if (!res.ok) {
				console.error('❌ Gagal fetch:', res.statusText);
				return;
			}

			const data = await res.json();
			console.log('✅ Data dari API:', data);
			peminjaman = data;
		} catch (err) {
			console.error('🔥 Error fetch:', err);
		}
	}

	// Function to format datetime to simple date
	function formatDate(dateString: string) {
		if (!dateString) return '-';

		const date = new Date(dateString);
		const options: Intl.DateTimeFormatOptions = {
			day: 'numeric',
			month: 'long',
			year: 'numeric',
			hour: '2-digit',
			minute: '2-digit',
			second: '2-digit',
			hour12: false // menggunakan format 24 jam
		};

		return new Intl.DateTimeFormat('id-ID', options).format(date);
	}

	// Function to get status badge color
	function getStatusColor(status: string) {
		switch (status?.toLowerCase()) {
			case 'sudah dikembalikan':
			case 'selesai':
				return 'bg-green-100 text-green-700 border border-green-200';
			case 'belum dikembalikan':
			case 'pending':
				return 'bg-yellow-100 text-yellow-700 border border-yellow-200';
			case 'terlambat':
			case 'overdue':
				return 'bg-red-100 text-red-700 border border-red-200';
			default:
				return 'bg-blue-100 text-blue-700 border border-blue-200';
		}
	}

	onMount(fetchData);

	$effect(() => {
		if (props.id) {
			fetchData();
		}
	});

	function Kembali() {
		dispatch('pageChange', { page: 'Detail' });
	}
</script>

{#if peminjaman}
	<div class="min-h-screen bg-gray-50 p-6">
		<div class="mx-auto max-w-6xl">
			<!-- Header -->
			<div class="mb-8">
				<div class="mb-2 flex items-center space-x-3">
					<div class="rounded-lg bg-gray-800 p-2">
						<svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
							></path>
						</svg>
					</div>
					<div>
						<h1 class="text-2xl font-bold text-gray-900">Detail Peminjaman</h1>
						<p class="text-gray-600">Informasi lengkap peminjaman barang</p>
					</div>
				</div>
			</div>

			<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
				<!-- Left Content - 2 columns -->
				<div class="space-y-6 lg:col-span-2">
					<!-- Kode Peminjaman Card -->
					<div class="rounded-2xl bg-white p-6 shadow-sm">
						<div class="flex items-center justify-between">
							<div>
								<h2 class="mb-2 text-lg font-semibold text-gray-900">Kode Peminjaman</h2>
								<p class="font-mono text-2xl font-bold text-gray-900">{peminjaman.kode_detail}</p>
							</div>
							<div class="text-right">
								<div class="mb-1 text-sm text-gray-500">Status</div>
								<span
									class="inline-flex items-center rounded-full px-3 py-1 text-sm font-medium {getStatusColor(
										peminjaman.status_pengambilan
									)}"
								>
									{peminjaman.status_pengambilan}
								</span>
							</div>
						</div>
					</div>

					<!-- Informasi Tanggal Card -->
					<div class="rounded-2xl bg-white p-6 shadow-sm">
						<div class="mb-6 flex items-center space-x-3">
							<svg
								class="h-5 w-5 text-gray-600"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
								></path>
							</svg>
							<h2 class="text-lg font-semibold text-gray-900">Informasi Tanggal</h2>
						</div>

						<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
							<div class="rounded-xl bg-gray-50 p-4">
								<div class="mb-2 text-sm font-medium text-gray-600">Tanggal Pinjam</div>
								<div class="text-lg font-semibold text-gray-900">
									{formatDate(peminjaman.waktu_pengambilan)}
								</div>
							</div>

							<div class="rounded-xl bg-gray-50 p-4">
								<div class="mb-2 text-sm font-medium text-gray-600">Tanggal Kembali</div>
								<div class="text-lg font-semibold text-gray-900">
									{formatDate(peminjaman.batas_ambil)}
								</div>
							</div>
						</div>
					</div>

					<!-- Detail Peminjaman Card -->
					<div class="rounded-2xl bg-white p-6 shadow-sm">
						<h2 class="mb-6 text-lg font-semibold text-gray-900">Detail Peminjaman</h2>

						<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
							<div class="flex justify-between border-b border-gray-100 py-3">
								<span class="text-gray-600">ID Peminjaman</span>
								<span class="font-medium text-gray-900">#{peminjaman.id_peminjaman}</span>
							</div>

							<div class="flex justify-between border-b border-gray-100 py-3">
								<span class="text-gray-600">ID Barang</span>
								<span class="font-medium text-gray-900">#{peminjaman.id_barang}</span>
							</div>

							<div class="flex justify-between border-b border-gray-100 py-3">
								<span class="text-gray-600">Jumlah</span>
								<span class="font-medium text-gray-900">{peminjaman.jumlah} Unit</span>
							</div>

							<div class="flex justify-between border-b border-gray-100 py-3">
								<span class="text-gray-600">Kode Detail</span>
								<span class="font-mono font-medium text-gray-900">{peminjaman.kode_detail}</span>
							</div>
						</div>
					</div>
				</div>

				<!-- Right Content - QR Code -->
				<div class="lg:col-span-1">
					<div class="sticky top-6 rounded-2xl bg-white p-6 text-center shadow-sm">
						<div class="mb-6 flex items-center justify-center space-x-2">
							<svg
								class="h-5 w-5 text-gray-600"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 16h4.01M12 8h4.01"
								></path>
							</svg>
							<h2 class="text-lg font-semibold text-gray-900">QR Code</h2>
						</div>

						<div class="flex flex-col items-center space-y-6">
							<!-- QR Code Container -->
							<div class="rounded-2xl border-2 border-gray-100 bg-white p-6 shadow-inner">
								<Qrcode value={peminjaman.kode_detail} />
							</div>

							<div class="space-y-2 text-center">
								<p class="max-w-xs text-sm leading-relaxed text-gray-500">
									Scan QR code untuk akses cepat informasi peminjaman
								</p>
							</div>
						</div>

						<!-- Action Buttons -->
						<div class="mt-8 space-y-3">
							<button
								class="w-full rounded-xl bg-blue-600 px-4 py-3 text-sm font-medium text-white transition duration-200 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
								onclick={() => dispatch('pageChange', { page: 'edit', id: peminjaman.id })}
							>
								Edit Peminjaman
							</button>

							<button
								class="w-full rounded-xl bg-green-600 px-4 py-3 text-sm font-medium text-white transition duration-200 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
							>
								Konfirmasi Pengambilan
							</button>

							<button
								class="w-full rounded-xl bg-gray-600 px-4 py-3 text-sm font-medium text-white transition duration-200 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
								onclick={Kembali}
							>
								Kembali ke Daftar
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
{:else}
	<h2>loading</h2>
{/if}

<style>
	:global(body) {
		font-family:
			'Inter',
			-apple-system,
			BlinkMacSystemFont,
			'Segoe UI',
			'Roboto',
			sans-serif;
	}
</style>
