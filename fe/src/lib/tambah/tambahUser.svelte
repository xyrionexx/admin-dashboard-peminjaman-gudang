<script lang="ts">
	import CryptoJS from 'crypto-js';
	import * as Select from '$lib/components/ui/select/index.js';
	import { createEventDispatcher, onMount } from 'svelte';
	const dispatch = createEventDispatcher<{ pageChange: { page: string; id?: number } }>();

	let value = $state('');
	let categories = ['Siswa', 'Guru', 'Pegawai'];
	let isLoading = $state(false);
	let successMessage = $state('');
	let errorMessage = $state('');
	let nis = $state('');
	let nama_siswa = $state('');
	let kelas = $state('');
	let kartu_pelajar = $state<File | null>(null);
	let no_telp = $state('');
	let nuptk = $state('');
	let nama_guru = $state('');
	let bidang = $state('');
	let email = $state('');
	let password = $state('');
	let id_pegawai = $state('');
	let nama_pegawai = $state('');

	function hashPassword(password: string): string {
		return CryptoJS.SHA256(password).toString();
	}

	async function tambahUser(event: Event, kategori: string) {
		event.preventDefault();
		isLoading = true;
		successMessage = '';
		errorMessage = '';
		const hashed = hashPassword(password);

		try {
			let endpoint = '';
			let bodyData: Record<string, any> = {};

			if (kategori === 'Siswa') {
				endpoint = 'tambah_siswa';
				bodyData = new FormData();
				bodyData.append('nis', nis);
				bodyData.append('nama_siswa', nama_siswa);
				bodyData.append('kelas', kelas);
				bodyData.append('no_telp', no_telp);
				bodyData.append('email', email);
				bodyData.append('password', hashed);
				if (kartu_pelajar) bodyData.append('kartu_pelajar', kartu_pelajar); // pastikan tidak null
			} else if (kategori === 'Guru') {
				endpoint = 'tambah_guru';
				bodyData = {
					nuptk,
					nama_guru,
					bidang,
					no_telp,
					email,
					password: hashed
				};
			} else if (kategori === 'Pegawai') {
				endpoint = 'tambah_pegawai';
				bodyData = {
					id_pegawai,
					nama_pegawai,
					bidang,
					no_telp,
					email,
					password: hashed
				};
			} else {
				errorMessage = 'Kategori tidak valid';
				throw new Error(errorMessage);
			}

			const response = await fetch(`https://api.borrowfy.site/api/user/${endpoint}`, {
				method: 'POST',
				body: bodyData instanceof FormData ? bodyData : JSON.stringify(bodyData),
				headers: bodyData instanceof FormData ? undefined : { 'Content-Type': 'application/json' }
			});

			if (response.ok) {
				const data = await response.json();
				console.log('✅ Data berhasil ditambahkan:', data);
				successMessage = `Data ${kategori} berhasil ditambahkan!`;

				nis = '';
				nama_siswa = '';
				kelas = '';
				kartu_pelajar = null;
				no_telp = '';
				nuptk = '';
				nama_guru = '';
				bidang = '';
			} else {
				const errText = await response.text();
				console.error('❌ Gagal menambahkan data:', errText);
				errorMessage = `Gagal menambahkan data ${kategori}. Silakan coba lagi.`;
			}
		} catch (error) {
			console.error('❌ Error:', error);
			errorMessage = 'Terjadi kesalahan. Periksa koneksi internet Anda.';
		} finally {
			isLoading = false;
		}
	}

	const handleKartuPelajar = (event: Event) => {
		const inputHTML = event.target as HTMLInputElement;
		if (inputHTML.files && inputHTML.files.length > 0) {
			kartu_pelajar = inputHTML.files[0];
		}
	};
</script>

<Select.Root type="single" bind:value>
	<Select.Trigger class="w-[180px] bg-white py-5">
		{value || 'Pilih kategori'}
	</Select.Trigger>
	<Select.Content>
		<Select.Group>
			<Select.Label>Category</Select.Label>
			{#each categories as kategori}
				<Select.Item value={kategori}>{kategori}</Select.Item>
			{/each}
		</Select.Group>
	</Select.Content>
</Select.Root>

<div class="mx-auto max-w-2xl">
	<div class="mb-8 text-center">
		<h1 class="text-foreground mb-2 text-3xl font-bold md:text-4xl">Tambah Barang</h1>
		<p class="text-muted text-balance">
			Isi semua kolom yang diperlukan untuk menambahkan barang baru ke inventori
		</p>
	</div>

	<div class="bg-card border-border rounded-lg border p-6 shadow-sm md:p-8">
		{#if successMessage}
			<div class="mb-6 rounded-md border border-green-200 bg-green-50 p-4">
				<div class="flex">
					<svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
						<path
							fill-rule="evenodd"
							d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
							clip-rule="evenodd"
						/>
					</svg>
					<p class="ml-3 text-sm font-medium text-green-800">{successMessage}</p>
				</div>
			</div>
		{/if}

		{#if errorMessage}
			<div class="mb-6 rounded-md border border-red-200 bg-red-50 p-4">
				<div class="flex">
					<svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
						<path
							fill-rule="evenodd"
							d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
							clip-rule="evenodd"
						/>
					</svg>
					<p class="ml-3 text-sm font-medium text-red-800">{errorMessage}</p>
				</div>
			</div>
		{/if}

		{#if value === 'Siswa'}
			<form onsubmit={(e) => tambahUser(e, 'Siswa')} class="space-y-6">
				<div class="space-y-2">
					<label for="nis" class="text-card-foreground block text-sm font-medium">
						NIS <span class="text-destructive">*</span>
					</label>
					<input
						id="nis"
						type="text"
						bind:value={nis}
						placeholder="Masukkan NIS"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="nama_siswa" class="text-card-foreground block text-sm font-medium">
						Nama Siswa <span class="text-destructive">*</span>
					</label>
					<input
						id="nama_siswa"
						type="text"
						bind:value={nama_siswa}
						placeholder="Masukkan Nama Siswa"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="kelas" class="text-card-foreground block text-sm font-medium">
						Kelas <span class="text-destructive">*</span>
					</label>
					<input
						id="kelas"
						type="text"
						bind:value={kelas}
						placeholder="Masukkan Kelas"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="kartu_pelajar" class="text-card-foreground block text-sm font-medium">
						Nomor Kartu Pelajar <span class="text-destructive">*</span>
					</label>
					<input
						id="kartu_pelajar"
						type="file"
						onchange={handleKartuPelajar}
						placeholder="Masukkan Foto Kartu Pelajar"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="no_telp" class="text-card-foreground block text-sm font-medium">
						No. Telepon <span class="text-destructive">*</span>
					</label>
					<input
						id="no_telp"
						type="text"
						bind:value={no_telp}
						placeholder="Masukkan No. Telepon"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="email" class="text-card-foreground block text-sm font-medium">
						Email <span class="text-destructive">*</span>
					</label>
					<input
						id="email"
						type="text"
						bind:value={email}
						placeholder="Masukkan Email"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="password" class="text-card-foreground block text-sm font-medium">
						Password <span class="text-destructive">*</span>
					</label>
					<input
						id="password"
						type="password"
						bind:value={password}
						placeholder="Masukkan Email"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="flex flex-col gap-3 pt-4 sm:flex-row sm:justify-end">
					<button
						type="button"
						onclick={() => dispatch('pageChange', { page: 'Pengguna' })}
						class="border-border bg-secondary text-secondary-foreground hover:bg-secondary/80 focus:ring-ring inline-flex items-center justify-center rounded-md border px-4 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					>
						Kembali
					</button>
					<button
						type="submit"
						disabled={isLoading}
						class="bg-primary text-primary-foreground hover:bg-primary/90 focus:ring-ring inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					>
						{#if isLoading}
							<svg class="mr-2 h-4 w-4 animate-spin" viewBox="0 0 24 24">
								<circle
									class="opacity-25"
									cx="12"
									cy="12"
									r="10"
									stroke="currentColor"
									stroke-width="4"
									fill="none"
								></circle>
								<path
									class="opacity-75"
									fill="currentColor"
									d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
								></path>
							</svg>
							Menyimpan...
						{:else}
							Tambah Siswa
						{/if}
					</button>
				</div>
			</form>
		{/if}

		{#if value === 'Pegawai'}
			<form onsubmit={(e) => tambahUser(e, 'Pegawai')} class="space-y-6">
				<div class="space-y-2">
					<label for="id_pegawai" class="text-card-foreground block text-sm font-medium">
						ID Pegawai <span class="text-destructive">*</span>
					</label>
					<input
						id="id_pegawai"
						type="text"
						bind:value={id_pegawai}
						placeholder="Masukkan ID Pegawai"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="nama_pegawai" class="text-card-foreground block text-sm font-medium">
						Nama Pegawai <span class="text-destructive">*</span>
					</label>
					<input
						id="nama_pegawai"
						type="text"
						bind:value={nama_pegawai}
						placeholder="Masukkan Nama Pegawai"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="bidang" class="text-card-foreground block text-sm font-medium">
						Bidang <span class="text-destructive">*</span>
					</label>
					<input
						id="bidang"
						type="text"
						bind:value={bidang}
						placeholder="Masukkan Bidang"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="no_telp" class="text-card-foreground block text-sm font-medium">
						No. Telepon <span class="text-destructive">*</span>
					</label>
					<input
						id="no_telp"
						type="text"
						bind:value={no_telp}
						placeholder="Masukkan No. Telepon"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="email" class="text-card-foreground block text-sm font-medium">
						Email <span class="text-destructive">*</span>
					</label>
					<input
						id="email"
						type="text"
						bind:value={email}
						placeholder="Masukkan Email"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="password" class="text-card-foreground block text-sm font-medium">
						Password <span class="text-destructive">*</span>
					</label>
					<input
						id="password"
						type="password"
						bind:value={password}
						placeholder="Masukkan Email"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="flex flex-col gap-3 pt-4 sm:flex-row sm:justify-end">
					<button
						type="button"
						onclick={() => dispatch('pageChange', { page: 'Pengguna' })}
						class="border-border bg-secondary text-secondary-foreground hover:bg-secondary/80 focus:ring-ring inline-flex items-center justify-center rounded-md border px-4 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					>
						Kembali
					</button>
					<button
						type="submit"
						disabled={isLoading}
						class="bg-primary text-primary-foreground hover:bg-primary/90 focus:ring-ring inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					>
						{#if isLoading}
							<svg class="mr-2 h-4 w-4 animate-spin" viewBox="0 0 24 24">
								<circle
									class="opacity-25"
									cx="12"
									cy="12"
									r="10"
									stroke="currentColor"
									stroke-width="4"
									fill="none"
								></circle>
								<path
									class="opacity-75"
									fill="currentColor"
									d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
								></path>
							</svg>
							Menyimpan...
						{:else}
							Tambah Siswa
						{/if}
					</button>
				</div>
			</form>
		{/if}

		{#if value === 'Guru'}
			<form onsubmit={(e) => tambahUser(e, 'Guru')} class="space-y-6">
				<div class="space-y-2">
					<label for="nuptk" class="text-card-foreground block text-sm font-medium">
						NUPTK <span class="text-destructive">*</span>
					</label>
					<input
						id="nuptk"
						type="text"
						bind:value={nuptk}
						placeholder="Masukkan NIS"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="nama_guru" class="text-card-foreground block text-sm font-medium">
						Nama Guru <span class="text-destructive">*</span>
					</label>
					<input
						id="nama_guru"
						type="text"
						bind:value={nama_guru}
						placeholder="Masukkan Nama Siswa"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="Bidang" class="text-card-foreground block text-sm font-medium">
						Bidang <span class="text-destructive">*</span>
					</label>
					<input
						id="bidang"
						type="text"
						bind:value={bidang}
						placeholder="Masukkan Kelas"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="space-y-2">
					<label for="no_telp" class="text-card-foreground block text-sm font-medium">
						No. Telepon <span class="text-destructive">*</span>
					</label>
					<input
						id="no_telp"
						type="text"
						bind:value={no_telp}
						placeholder="Masukkan No. Telepon"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>
				<div class="space-y-2">
					<label for="email" class="text-card-foreground block text-sm font-medium">
						Email <span class="text-destructive">*</span>
					</label>
					<input
						id="email"
						type="text"
						bind:value={email}
						placeholder="Masukkan Email"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>
				<div class="space-y-2">
					<label for="password" class="text-card-foreground block text-sm font-medium">
						password <span class="text-destructive">*</span>
					</label>
					<input
						id="password"
						type="text"
						bind:value={password}
						placeholder="Masukkan Password"
						required
						disabled={isLoading}
						class="border-border bg-input placeholder:text-muted focus:border-accent focus:ring-ring w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>

				<div class="flex flex-col gap-3 pt-4 sm:flex-row sm:justify-end">
					<button
						type="button"
						onclick={() => dispatch('pageChange', { page: 'Pengguna' })}
						class="border-border bg-secondary text-secondary-foreground hover:bg-secondary/80 focus:ring-ring inline-flex items-center justify-center rounded-md border px-4 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					>
						Kembali
					</button>
					<button
						type="submit"
						disabled={isLoading}
						class="bg-primary text-primary-foreground hover:bg-primary/90 focus:ring-ring inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50"
					>
						{#if isLoading}
							<svg class="mr-2 h-4 w-4 animate-spin" viewBox="0 0 24 24">
								<circle
									class="opacity-25"
									cx="12"
									cy="12"
									r="10"
									stroke="currentColor"
									stroke-width="4"
									fill="none"
								></circle>
								<path
									class="opacity-75"
									fill="currentColor"
									d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
								></path>
							</svg>
							Menyimpan...
						{:else}
							Tambah Siswa
						{/if}
					</button>
				</div>
			</form>
		{/if}
	</div>
</div>
