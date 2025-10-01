<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import Icon from '@iconify/svelte';

	export let id: number;
	const dispatch = createEventDispatcher<{ pageChange: { page: string; id?: number } }>();

	let nama = '';
	let jumlah: number = 0;
	let kategori = '';
	let deskripsi = '';
	let isLoading = false;
	let img: File | null = null;
	let currentImage: string | null = null;
	let imagePreview: string | null = null;
	let successMessage = '';
	let errorMessage = '';

	onMount(async () => {
		if (!id) return;
		try {
			const res = await fetch(`https://api.borrowfy.site/api/barang/${id}/`);
			if (!res.ok) throw new Error('Data tidak ditemukan');
			const data = await res.json();
			nama = data.nama_barang;
			jumlah = data.jumlah;
			kategori = data.kategori;
			deskripsi = data.deskripsi;
			
			// Check if there's an existing image
			if (data.img) {
				currentImage = 'data:image/png;base64,' + data.img;
			}
		} catch (err) {
			console.error(err);
			errorMessage = 'Gagal mengambil data barang';
		}
	});

	async function saveUpdate(event: Event) {
		event.preventDefault();
		isLoading = true;
		successMessage = '';
		errorMessage = '';

		try {
			// If we have a new image, use FormData to support file upload
			if (img) {
				const formData = new FormData();
				formData.append('nama_barang', nama);
				formData.append('jumlah', jumlah.toString());
				formData.append('kategori', kategori);
				formData.append('deskripsi', deskripsi);
				formData.append('img', img);
				
				const res = await fetch(`https://api.borrowfy.site/api/barang/${id}/`, {
					method: 'PUT',
					body: formData
				});
				
				if (!res.ok) throw new Error('Gagal update data');
				successMessage = 'Data berhasil diperbarui';
				setTimeout(() => dispatch('pageChange', { page: 'Barang' }), 1500);
			} else {
				// If no new image, use JSON
				const res = await fetch(`https://api.borrowfy.site/api/barang/${id}/`, {
					method: 'PUT',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ nama_barang: nama, jumlah, kategori, deskripsi })
				});
				
				if (!res.ok) throw new Error('Gagal update data');
				successMessage = 'Data berhasil diperbarui';
				setTimeout(() => dispatch('pageChange', { page: 'Barang' }), 1500);
			}
		} catch (err) {
			console.error(err);
			errorMessage = 'Terjadi kesalahan saat update';
		} finally {
			isLoading = false;
		}
	}

	function cancel() {
		dispatch('pageChange', { page: 'Barang' });
	}

	// Penanganan file input dengan tipe aman untuk TS dan menambahkan preview
	const handleFileChange = (event: Event) => {
		const inputHTML = event.target as HTMLInputElement;
		if (inputHTML.files && inputHTML.files.length > 0) {
			img = inputHTML.files[0];
			
			// Revoke previous preview URL if exists
			if (imagePreview) {
				URL.revokeObjectURL(imagePreview);
			}
			
			// Membuat URL untuk preview gambar
			imagePreview = URL.createObjectURL(img);
		}
	};

	// Hapus preview ketika komponen unmount
	function cleanup() {
		if (imagePreview) {
			URL.revokeObjectURL(imagePreview);
		}
	}
</script>

<div class="mx-auto my-8 max-w-2xl rounded-xl border border-blue-50 bg-white p-8 shadow-lg">
	<h1 class="mb-6 text-center text-3xl font-semibold tracking-tight text-blue-800">
		Update Barang
	</h1>
	
	{#if errorMessage}
		<div class="mb-6 rounded-md bg-red-50 p-4 text-red-700">
			<div class="flex items-center">
				<Icon icon="mdi:alert-circle" class="mr-2" width="20" height="20" />
				<span>{errorMessage}</span>
			</div>
		</div>
	{/if}
	
	{#if successMessage}
		<div class="mb-6 rounded-md bg-green-50 p-4 text-green-700">
			<div class="flex items-center">
				<Icon icon="mdi:check-circle" class="mr-2" width="20" height="20" />
				<span>{successMessage}</span>
			</div>
		</div>
	{/if}

	<form onsubmit={(e) => { e.preventDefault(); saveUpdate(e); }} class="space-y-6">
		<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
			<div class="space-y-2">
				<label for="nama" class="block text-sm font-medium text-gray-700">Nama Barang</label>
				<input
					id="nama"
					type="text"
					bind:value={nama}
					required
					class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
				/>
			</div>

			<div class="space-y-2">
				<label for="jumlah" class="block text-sm font-medium text-gray-700">Jumlah</label>
				<input
					id="jumlah"
					type="number"
					bind:value={jumlah}
					required
					class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
				/>
			</div>

			<div class="space-y-2">
				<label for="kategori" class="block text-sm font-medium text-gray-700">Kategori</label>
				<input
					id="kategori"
					type="text"
					bind:value={kategori}
					required
					class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
				/>
			</div>
		</div>

		<div class="space-y-2">
			<label for="deskripsi" class="block text-sm font-medium text-gray-700">Deskripsi</label>
			<textarea
				id="deskripsi"
				bind:value={deskripsi}
				rows="3"
				required
				class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
			></textarea>
		</div>
		
		<!-- Image Upload Section -->
		<div class="space-y-2">
			<label for="img" class="block text-sm font-medium text-gray-700">Gambar</label>
			<div class="flex flex-col space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0">
				<!-- Upload Area -->
				<div class="flex-1">
					<div class="relative flex h-32 w-full cursor-pointer items-center justify-center rounded-md border-2 border-dashed border-blue-200 bg-blue-50/20 hover:bg-blue-50/40">
						<input
							id="img"
							type="file"
							accept="image/*"
							onchange={handleFileChange}
							class="absolute inset-0 h-full w-full cursor-pointer opacity-0"
						/>
						<div class="flex flex-col items-center justify-center text-center">
							<Icon icon="mdi:cloud-upload" class="mb-2 text-blue-500" width="24" height="24" />
							<span class="text-sm font-medium text-gray-600">Klik untuk upload gambar baru</span>
							<span class="mt-1 text-xs text-gray-500">(Opsional)</span>
						</div>
					</div>
				</div>
				
				<!-- Preview Area -->
				<div class="flex-1">
					{#if imagePreview}
						<!-- New image preview -->
						<div class="relative">
							<img
								src={imagePreview}
								alt="Preview gambar baru"
								class="h-32 w-full rounded-md border border-blue-200 object-contain"
							/>
							<div class="absolute -right-2 -top-2 flex items-center justify-center">
								<button
									type="button"
									class="flex h-6 w-6 items-center justify-center rounded-full bg-red-500 text-white hover:bg-red-600"
									onclick={() => {
										if (imagePreview) {
											URL.revokeObjectURL(imagePreview);
										}
										imagePreview = null;
										img = null;
									}}
								>
									<Icon icon="mdi:close" width="16" height="16" />
								</button>
							</div>
						</div>
					{:else if currentImage}
						<!-- Current image preview -->
						<div class="relative">
							<img
								src={currentImage}
								alt="Gambar saat ini"
								class="h-32 w-full rounded-md border border-blue-200 object-contain"
							/>
							<div class="absolute top-0 left-0 flex h-full w-full items-center justify-center">
								<span class="rounded bg-blue-800/80 px-2 py-1 text-xs text-white">Gambar Saat Ini</span>
							</div>
						</div>
					{:else}
						<!-- No image -->
						<div class="flex h-32 w-full items-center justify-center rounded-md border border-blue-100 bg-blue-50/20">
							<span class="text-sm text-gray-500">Tidak ada gambar</span>
						</div>
					{/if}
				</div>
			</div>
		</div>

		<div class="flex flex-col-reverse gap-3 pt-4 sm:flex-row sm:justify-between">
			<button
				type="button"
				class="focus:ring-3 rounded-lg border border-slate-200 bg-slate-100 px-6 py-3 font-medium text-slate-600 transition-all duration-200 hover:-translate-y-0.5 hover:bg-slate-200 hover:text-slate-700 hover:shadow-md focus:outline-none focus:ring-slate-200 active:translate-y-0"
				onclick={cancel}
			>
				<div class="flex items-center">
					<Icon icon="mdi:arrow-left" class="mr-2" width="16" height="16" />
					Batal
				</div>
			</button>
			
			<button
				type="submit"
				disabled={isLoading}
				onclick={saveUpdate}
				class="focus:ring-3 rounded-lg bg-gradient-to-r from-blue-500 to-blue-700 px-6 py-3 font-medium text-white transition-all duration-200 hover:-translate-y-0.5 hover:from-blue-600 hover:to-blue-800 hover:shadow-lg focus:outline-none focus:ring-blue-300 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-70"
			>
				<div class="flex items-center">
					{#if isLoading}
						<Icon icon="mdi:loading" class="mr-2 animate-spin" width="16" height="16" />
						Menyimpan...
					{:else}
						<Icon icon="mdi:content-save" class="mr-2" width="16" height="16" />
						Simpan Perubahan
					{/if}
				</div>
			</button>
		</div>
	</form>
</div>
