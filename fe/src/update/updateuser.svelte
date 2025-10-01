<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';

	const { id, kategori } = $props<{
		id: string;
		kategori: string;
	}>();

	const dispatch = createEventDispatcher<{
		pageChange: { page: string; id?: string; kategori?: string };
	}>();

	// Gunakan $state agar reactive
	let nis = $state('');
	let nama = $state('');
	let kelas = $state('');
	let nuptk = $state('');
	let bidang = $state('');
	let no_telp = $state('');
	let kartu_pelajar = $state<File | null>(null);
	let kartu_pelajar_url = $state('');
	let imagePreview = $state<string | null>(null);
	let email = $state('');
	let password = $state('');
	let id_pegawai = $state('');
	let nama_pegawai = $state('');
	let errorMessage = $state('');
	let successMessage = $state('');
	let isLoading = $state(false);

	async function fetchData() {
		isLoading = true;
		if (!id) return;
		try {
			const url = `https://api.borrowfy.site/api/update/${kategori}/${id}/`;
			const res = await fetch(url);
			if (!res.ok) throw new Error('Data tidak ditemukan');
			const data = await res.json();

			if (kategori === 'Siswa') {
				nis = data.nis;
				nama = data.nama_siswa || data.nama;
				kelas = data.kelas;
				no_telp = data.no_telp;
				email = data.email;

				// Set kartu pelajar URL jika ada
				if (data.kartu_pelajar) {
					kartu_pelajar_url = data.kartu_pelajar;
					imagePreview = data.kartu_pelajar;
				}
			} else if (kategori === 'Guru') {
				nuptk = data.nuptk;
				nama = data.nama_guru || data.nama;
				bidang = data.bidang;
				no_telp = data.no_telp;
				email = data.email;
			} else if (kategori === 'Pegawai') {
				id_pegawai = data.id_pegawai;
				nama_pegawai = data.nama_pegawai;
				bidang = data.bidang;
				no_telp = data.no_telp;
				email = data.email;
			}
			errorMessage = '';
		} catch (err) {
			console.error(err);
			errorMessage = 'Gagal mengambil data pengguna';
		} finally {
			isLoading = false;
		}
	}

	// Handle file input change for kartu_pelajar
	function handleImageChange(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input.files && input.files.length > 0) {
			kartu_pelajar = input.files[0];

			// Create preview
			imagePreview = URL.createObjectURL(kartu_pelajar);
		}
	}

	async function updateUser(event: Event) {
		event.preventDefault();
		isLoading = true;
		successMessage = '';
		errorMessage = '';

		try {
			const url = `https://api.borrowfy.site/api/update/${kategori}/${id}/`;

			if (kategori === 'Siswa') {
				const formData = new FormData();
				formData.append('nis', nis);
				formData.append('nama_siswa', nama);
				formData.append('kelas', kelas);
				formData.append('no_telp', no_telp);
				formData.append('email', email);

				// Hanya tambahkan password jika diisi
				if (password) {
					formData.append('password', password);
				}

				// Tambahkan file kartu pelajar jika ada yang baru diupload
				if (kartu_pelajar) {
					formData.append('kartu_pelajar', kartu_pelajar);
				}

				const response = await fetch(url, {
					method: 'PUT',
					body: formData
				});

				if (response.ok) {
					successMessage = 'Data siswa berhasil diperbarui!';
					setTimeout(() => dispatch('pageChange', { page: 'Pengguna' }), 1500);
				} else {
					const errorData = await response.json();
					errorMessage = errorData.message || 'Gagal memperbarui data';
				}
			} else if (kategori === 'Guru') {
				const response = await fetch(url, {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						nuptk,
						nama_guru: nama,
						bidang,
						no_telp,
						email,
						password: password || undefined
					})
				});

				if (response.ok) {
					successMessage = 'Data guru berhasil diperbarui!';
					setTimeout(() => dispatch('pageChange', { page: 'Pengguna' }), 1500);
				} else {
					const errorData = await response.json();
					errorMessage = errorData.message || 'Gagal memperbarui data';
				}
			} else if (kategori === 'Pegawai') {
				const response = await fetch(url, {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						id_pegawai,
						nama_pegawai,
						bidang,
						no_telp,
						email,
						password: password || undefined
					})
				});

				if (response.ok) {
					successMessage = 'Data pegawai berhasil diperbarui!';
					setTimeout(() => dispatch('pageChange', { page: 'Pengguna' }), 1500);
				} else {
					const errorData = await response.json();
					errorMessage = errorData.message || 'Gagal memperbarui data';
				}
			}
		} catch (err) {
			console.error(err);
			errorMessage = 'Terjadi kesalahan saat memperbarui data';
		} finally {
			isLoading = false;
		}
	}

	onMount(() => {
		fetchData();
	});

	function goBack() {
		dispatch('pageChange', { page: 'Pengguna' });
	}
</script>

<!-- Form update dengan UI yang bagus -->
<div class="min-h-screen bg-gray-50 p-6">
	<div class="mx-auto max-w-2xl rounded-xl bg-white p-8 shadow-sm">
		<div class="mb-6">
			<h2 class="text-2xl font-semibold text-gray-800">Update {kategori}</h2>
			<p class="mt-1 text-sm text-gray-500">
				Silakan isi formulir di bawah untuk memperbarui data {kategori}
			</p>
		</div>

		{#if isLoading}
			<div class="my-8 flex justify-center">
				<div class="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-500"></div>
			</div>
		{:else}
			{#if successMessage}
				<div class="mb-4 rounded border border-green-400 bg-green-100 px-4 py-3 text-green-700">
					{successMessage}
				</div>
			{/if}

			{#if errorMessage}
				<div class="mb-4 rounded border border-red-400 bg-red-100 px-4 py-3 text-red-700">
					{errorMessage}
				</div>
			{/if}

			<form onsubmit={updateUser} class="space-y-5">
				{#if kategori === 'Siswa'}
					<div class="">
						<label for="nis" class="block text-sm font-medium text-gray-700">NIS</label>
						<input
							id="nis"
							type="text"
							bind:value={nis}
							required
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<label for="nama" class="block text-sm font-medium text-gray-700">Nama</label>
						<input
							id="nama"
							type="text"
							bind:value={nama}
							required
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<label for="kelas" class="block text-sm font-medium text-gray-700">Kelas</label>
						<input
							id="kelas"
							type="text"
							bind:value={kelas}
							required
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<label for="no_telp" class="block text-sm font-medium text-gray-700">No Telp</label>
						<input
							id="no_telp"
							type="text"
							bind:value={no_telp}
							required
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<div class="">
							<label for="email" class="block text-sm font-medium text-gray-700">Email</label>
							<input
								id="email"
								type="email"
								bind:value={email}
								class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
							/>
						</div>
					</div>

					<div class="">
						<label for="password" class="block text-sm font-medium text-gray-700"
							>Password (kosongkan jika tidak ingin mengganti)</label
						>
						<input
							id="password"
							type="password"
							bind:value={password}
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<!-- Kartu Pelajar Upload dan Preview -->
					<div class="space-y-2">
						<label for="kartu_pelajar_input" class="block text-sm font-medium text-gray-700"
							>Kartu Pelajar</label
						>
						<div class="flex flex-col space-y-4 md:flex-row md:space-x-4 md:space-y-0">
							<div class="flex-1">
								<div
									class="relative flex h-32 w-full cursor-pointer items-center justify-center rounded-md border-2 border-dashed border-gray-300 hover:bg-gray-50"
								>
									<input
										id="kartu_pelajar_input"
										type="file"
										accept="image/*"
										onchange={handleImageChange}
										class="absolute inset-0 h-full w-full cursor-pointer opacity-0"
									/>
									<div class="text-center">
										<svg
											class="mx-auto h-10 w-10 text-gray-400"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
											/>
										</svg>
										<p class="mt-1 text-sm text-gray-500">Klik untuk pilih gambar</p>
										<p class="text-xs text-gray-400">PNG, JPG, JPEG hingga 2MB</p>
									</div>
								</div>
							</div>

							<!-- Preview Gambar -->
							<div class="flex-1">
								{#if imagePreview}
									<div class="relative h-32 w-full">
										<img
											src={imagePreview}
											alt="Kartu Pelajar"
											class="h-32 w-full rounded border object-contain"
										/>
									</div>
								{:else}
									<div
										class="flex h-32 w-full items-center justify-center rounded-md border border-gray-300 bg-gray-50"
									>
										<span class="text-sm text-gray-500">Preview gambar</span>
									</div>
								{/if}
							</div>
						</div>
						<p class="mt-1 text-xs text-gray-500">
							Unggah gambar kartu pelajar baru jika ingin mengganti yang lama
						</p>
					</div>
				{:else if kategori === 'Guru'}
					<div class="">
						<label for="nuptk_guru" class="block text-sm font-medium text-gray-700">NUPTK </label>
						<input
							id="nuptk_guru"
							type="text"
							bind:value={nuptk}
							readonly
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<label for="nama_guru" class="block text-sm font-medium text-gray-700">Nama</label>
						<input
							id="nama_guru"
							type="text"
							bind:value={nama}
							required
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<label for="bidang_guru" class="block text-sm font-medium text-gray-700">Bidang</label>
						<input
							id="bidang_guru"
							type="text"
							bind:value={bidang}
							required
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<label for="no_telp_guru" class="block text-sm font-medium text-gray-700">No Telp</label
						>
						<input
							id="no_telp_guru"
							type="text"
							bind:value={no_telp}
							required
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>
					<div class="">
						<label for="email_guru" class="block text-sm font-medium text-gray-700">Email</label>
						<input
							id="email_guru"
							type="email"
							bind:value={email}
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<label for="password_guru" class="block text-sm font-medium text-gray-700"
							>Password (kosongkan jika tidak ingin mengganti)</label
						>
						<input
							id="password_guru"
							type="password"
							bind:value={password}
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>
				{:else if kategori === 'Pegawai'}
					<div class="">
						<label for="id_pegawai_field" class="block text-sm font-medium text-gray-700"
							>ID Pegawai
						</label>
						<input
							id="id_pegawai_field"
							type="text"
							bind:value={id_pegawai}
							readonly
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<label for="nama_pegawai_field" class="block text-sm font-medium text-gray-700"
							>Nama</label
						>
						<input
							id="nama_pegawai_field"
							type="text"
							bind:value={nama_pegawai}
							required
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<label for="bidang_pegawai" class="block text-sm font-medium text-gray-700"
							>Bidang</label
						>
						<input
							id="bidang_pegawai"
							type="text"
							bind:value={bidang}
							required
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<label for="no_telp_pegawai" class="block text-sm font-medium text-gray-700"
							>No Telp</label
						>
						<input
							id="no_telp_pegawai"
							type="text"
							bind:value={no_telp}
							required
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>
					<div class="">
						<label for="email_pegawai" class="block text-sm font-medium text-gray-700">Email</label>
						<input
							id="email_pegawai"
							type="email"
							bind:value={email}
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>

					<div class="">
						<label for="password_pegawai" class="block text-sm font-medium text-gray-700"
							>Password (kosongkan jika tidak ingin mengganti)</label
						>
						<input
							id="password_pegawai"
							type="password"
							bind:value={password}
							class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
						/>
					</div>
				{/if}

				<button
					type="submit"
					disabled={isLoading}
					class="focus:ring-3 rounded-lg bg-gradient-to-r from-blue-500 to-blue-700 px-6 py-3 font-medium text-white transition-all duration-200 hover:-translate-y-0.5 hover:from-blue-600 hover:to-blue-800 hover:shadow-lg focus:outline-none focus:ring-blue-300 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-70"
				>
					{#if isLoading}
						Menyimpan...
					{:else}
						Simpan
					{/if}
				</button>
			</form>

			<button onclick={goBack} class="mt-4 rounded bg-blue-500 px-4 py-2 text-white">
				Kembali
			</button>
		{/if}
	</div>
</div>
