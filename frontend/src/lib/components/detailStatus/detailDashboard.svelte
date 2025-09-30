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
			const res = await fetch(`http://127.0.0.1:8000/api/peminjaman/${props.id}/`);
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

	onMount(fetchData);

	$effect(() => {
		if (props.id) {
			fetchData();
		}
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

	function getStatusColor(
		status: 'Sedang Diambil' | 'Masih Dipinjam' | 'Dibatalkan' | 'Selesai'
	): string {
		switch (status) {
			case 'Sedang Diambil':
				return 'bg-yellow-100 text-yellow-800 border-yellow-200';
			case 'Selesai':
				return 'bg-green-100 text-green-800 border-green-200';
			case 'Dibatalkan':
				return 'bg-red-100 text-red-800 border-red-200';
			case 'Masih Dipinjam':
				return 'bg-blue-100 text-red-800 border-blue-200';
			default:
				return 'bg-gray-100 text-gray-800 border-gray-200';
		}
	}

	function getBorrowerInfo() {
		if (peminjaman.nis?.trim()) {
			return { type: 'Siswa', id: peminjaman.nis, icon: '👨‍🎓' };
		} else if (peminjaman.nuptk?.trim()) {
			return { type: 'Guru', id: peminjaman.nuptk, icon: '👨‍🏫' };
		} else if (peminjaman.id_pegawai?.trim()) {
			return { type: 'Pegawai', id: peminjaman.id_pegawai, icon: '👨‍💼' };
		}
		return { type: 'Unknown', id: '-', icon: '❓' };
	}

	let borrowerInfo = $derived(getBorrowerInfo());
	function Kembali() {
		dispatch('pageChange', { page: 'Aktivitas' });
	}
</script>

{#if peminjaman}
	<div class="min-h-screen bg-gradient-to-br from-blue-50 to-white p-4 md:p-8">
		<div class="mx-auto max-w-4xl">
			<!-- Header -->
			<div class="mb-8">
				<div class="mb-2 flex items-center gap-3">
					<div class="bg-primary flex h-10 w-10 items-center justify-center rounded-lg">
						<svg
							class="text-primary-foreground h-6 w-6"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
							/>
						</svg>
					</div>
					<div>
						<h1 class="text-foreground text-3xl font-bold">Detail Peminjaman</h1>
						<p class="text-muted-foreground">Informasi lengkap peminjaman barang</p>
					</div>
				</div>
			</div>

			<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
				<!-- Main Info Card -->
				<div class="space-y-6 lg:col-span-2">
					<!-- Loan Code & Status -->
					<div class="bg-card border-border rounded-xl border p-6 shadow-sm">
						<div class="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
							<div>
								<h2 class="text-card-foreground mb-1 text-xl font-semibold">Kode Peminjaman</h2>
								<p class="text-primary font-mono text-2xl font-bold">{peminjaman.kode_pinjam}</p>
							</div>
							<div class="flex flex-col items-start gap-2 sm:items-end">
								<span class="text-muted-foreground text-sm">Status</span>
								<span
									class="rounded-full border px-3 py-1 text-sm font-medium {getStatusColor(
										peminjaman.status_pinjam
									)}"
								>
									{peminjaman.status_pinjam}
								</span>
							</div>
						</div>
					</div>

					<!-- Date Information -->
					<div class="bg-card border-border rounded-xl border p-6 shadow-sm">
						<h3 class="text-card-foreground mb-4 flex items-center gap-2 text-lg font-semibold">
							<svg
								class="text-primary h-5 w-5"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
								/>
							</svg>
							Informasi Tanggal
						</h3>
						<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
							<div class="bg-muted rounded-lg p-4">
								<div class="text-muted-foreground mb-1 text-sm">Tanggal Pinjam</div>
								<div class="text-card-foreground font-semibold">
									{formatDate(peminjaman.tanggal_pinjam)}
								</div>
							</div>
							<div class="bg-muted rounded-lg p-4">
								<div class="text-muted-foreground mb-1 text-sm">Tanggal Kembali</div>
								<div class="text-card-foreground font-semibold">
									{formatDate(peminjaman.tanggal_kembali)}
								</div>
							</div>
						</div>
					</div>

					<!-- Borrower Information -->
					<div class="bg-card border-border rounded-xl border p-6 shadow-sm">
						<h3 class="text-card-foreground mb-4 flex items-center gap-2 text-lg font-semibold">
							<svg
								class="text-primary h-5 w-5"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
								/>
							</svg>
							Informasi Peminjam
						</h3>
						<div class="bg-muted rounded-lg p-4">
							<div class="flex items-center gap-3">
								<span class="text-2xl">{borrowerInfo.icon}</span>
								<div>
									<div class="text-muted-foreground text-sm">{borrowerInfo.type}</div>
									<div class="text-card-foreground font-mono font-semibold">{borrowerInfo.id}</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- QR Code Card -->
				<div class="lg:col-span-1">
					<div class="bg-card border-border sticky top-8 rounded-xl border p-6 shadow-sm">
						<h3 class="text-card-foreground mb-4 flex items-center gap-2 text-lg font-semibold">
							<svg
								class="text-primary h-5 w-5"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"
								/>
							</svg>
							QR Code
						</h3>
						<div class="flex justify-center">
							<Qrcode value={peminjaman.kode_pinjam} />
						</div>
						<p class="text-muted-foreground mt-4 text-center text-sm">
							Scan QR code untuk akses cepat informasi peminjaman
						</p>
					</div>
				</div>
			</div>

			<!-- Action Buttons -->
			<div class="mt-8 flex flex-wrap justify-center gap-3 lg:justify-start">
				<button
					class="bg-primary text-primary-foreground hover:bg-primary/90 flex items-center gap-2 rounded-lg px-6 py-2 font-medium transition-colors"
				>
					<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
						/>
					</svg>
					Edit Peminjaman
				</button>
				<button
					class="bg-secondary text-secondary-foreground hover:bg-secondary/90 flex items-center gap-2 rounded-lg px-6 py-2 font-medium transition-colors"
				>
					<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
						/>
					</svg>
					Print Detail
				</button>
				<button
					class="bg-muted text-muted-foreground hover:bg-muted/80 flex items-center gap-2 rounded-lg px-6 py-2 font-medium transition-colors"
					onclick={Kembali}
				>
					<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M10 19l-7-7m0 0l7-7m-7 7h18"
						/>
					</svg>
					Kembali
				</button>
			</div>
		</div>
	</div>
{:else}
	<p>Loading...</p>
{/if}
