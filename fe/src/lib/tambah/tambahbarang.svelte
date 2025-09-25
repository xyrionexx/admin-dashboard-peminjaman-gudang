<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Icon from '@iconify/svelte';

	const dispatch = createEventDispatcher<{ pageChange: { page: string; id?: number } }>();

	let id_barang = '';
	let nama_barang = '';
	let deskripsi = '';
	let jumlah = 0;
	let kategori = '';
	let img: File | null = null;
	let imagePreview: string | null = null;
	let isLoading = false;
	let successMessage = '';
	let errorMessage = '';

	async function tambah_barang(event: Event) {
		event.preventDefault();
		isLoading = true;
		successMessage = '';
		errorMessage = '';

		try {
			const bodyData = new FormData();
			bodyData.append('id_barang', id_barang);
			bodyData.append('nama_barang', nama_barang);
			bodyData.append('jumlah', jumlah.toString());
			bodyData.append('kategori', kategori);
			bodyData.append('deskripsi', deskripsi);
			if (img) bodyData.append('img', img);

			const response = await fetch('http://127.0.0.1:8000/api/barang/tambah_barang/', {
				method: 'POST',
				body: bodyData instanceof FormData ? bodyData : JSON.stringify(bodyData)
			});

			if (response.ok) {
				const data = await response.json();
				successMessage = 'Barang berhasil ditambahkan!';

				// Reset form
				id_barang = '';
				nama_barang = '';
				jumlah = 0;
				kategori = '';
				deskripsi = '';
				img = null;
				imagePreview = null;
			} else {
				const err = await response.json();
				errorMessage = err.detail || 'Gagal menambahkan barang.';
			}
		} catch (error) {
			console.error('❌ Error:', error);
			errorMessage = 'Terjadi kesalahan. Periksa koneksi internet Anda.';
		} finally {
			isLoading = false;
		}
	}

	// Penanganan file input dengan tipe aman untuk TS dan menambahkan preview
	const handleFileChange = (event: Event) => {
		const inputHTML = event.target as HTMLInputElement;
		if (inputHTML.files && inputHTML.files.length > 0) {
			img = inputHTML.files[0];

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

<div class="min-h-screen bg-gray-50 p-6">
	<div class="mx-auto max-w-2xl rounded-xl bg-white p-8 shadow-sm">
		<div class="mb-6">
			<h2 class="text-2xl font-semibold text-gray-800">Tambah User</h2>
			<p class="mt-1 text-sm text-gray-500">
				Silakan isi formulir di bawah untuk menambahkan barang baru ke inventori
			</p>
		</div>

		<form onsubmit={tambah_barang} class="space-y-5">
			<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
				<div class="space-y-2">
					<label for="id_barang" class="block text-sm font-medium text-gray-700">ID Barang</label>
					<input
						id="id_barang"
						type="text"
						bind:value={id_barang}
						required
						class="w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
					/>
				</div>

				<div class="space-y-2">
					<label for="nama_barang" class="block text-sm font-medium text-gray-700"
						>Nama Barang</label
					>
					<input
						id="nama_barang"
						type="text"
						bind:value={nama_barang}
						required
						class="w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
					/>
				</div>

				<div class="space-y-2">
					<label for="jumlah" class="block text-sm font-medium text-gray-700">Jumlah</label>
					<input
						id="jumlah"
						type="number"
						bind:value={jumlah}
						min="0"
						required
						class="w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
					/>
				</div>

				<div class="space-y-2">
					<label for="kategori" class="block text-sm font-medium text-gray-700">Kategori</label>
					<input
						id="kategori"
						type="text"
						bind:value={kategori}
						required
						class="w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
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
					class="w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
				></textarea>
			</div>

			<div class="space-y-2">
				<label for="img" class="block text-sm font-medium text-gray-700">Gambar</label>
				<div class="flex flex-col space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0">
					<div class="flex-1">
						<div
							class="relative flex h-32 w-full cursor-pointer items-center justify-center rounded-md border-2 border-dashed border-gray-300 hover:bg-gray-50"
						>
							<input
								id="img"
								type="file"
								accept="image/*"
								onchange={handleFileChange}
								class="absolute inset-0 h-full w-full cursor-pointer opacity-0"
							/>
							<div class="flex flex-col items-center justify-center text-center">
								<Icon icon="mdi:cloud-upload" class="mb-2 text-blue-500" width="24" height="24" />
								<span class="text-sm font-medium text-gray-600">Klik untuk memilih gambar</span>
								<span class="mt-1 text-xs text-gray-500">(JPG, PNG, atau GIF)</span>
							</div>
						</div>
					</div>

					<!-- Preview Gambar -->
					<div class="flex-1">
						{#if imagePreview}
							<div class="relative">
								<img
									src={imagePreview}
									alt="Preview gambar"
									class="h-32 w-full rounded-md border object-contain"
								/>
								<button
									type="button"
									class="absolute -right-2 -top-2 flex h-6 w-6 items-center justify-center rounded-full bg-red-500 text-white hover:bg-red-600"
									onclick={() => {
										URL.revokeObjectURL(imagePreview as string);
										imagePreview = null;
										img = null;
									}}
								>
									<Icon icon="mdi:close" width="16" height="16" />
								</button>
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
			</div>

			{#if successMessage}
				<div class="rounded-md bg-green-50 p-4 text-green-700">
					<div class="flex items-center">
						<Icon icon="mdi:check-circle" class="mr-2" width="20" height="20" />
						<span>{successMessage}</span>
					</div>
				</div>
			{/if}

			{#if errorMessage}
				<div class="rounded-md bg-red-50 p-4 text-red-700">
					<div class="flex items-center">
						<Icon icon="mdi:alert-circle" class="mr-2" width="20" height="20" />
						<span>{errorMessage}</span>
					</div>
				</div>
			{/if}

			<div class="flex flex-col-reverse gap-3 sm:flex-row sm:justify-between">
				<button
					type="button"
					onclick={() => dispatch('pageChange', { page: 'Barang' })}
					class="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
				>
					<Icon icon="mdi:arrow-left" class="mr-2" width="16" height="16" />
					Kembali
				</button>

				<button
					type="submit"
					disabled={isLoading}
					class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:bg-blue-400"
				>
					{#if isLoading}
						<Icon icon="mdi:loading" class="mr-2 animate-spin" width="16" height="16" />
						Menyimpan...
					{:else}
						<Icon icon="mdi:plus" class="mr-2" width="16" height="16" />
						Tambah Barang
					{/if}
				</button>
			</div>
		</form>
	</div>
</div>
