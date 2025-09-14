<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher<{ pageChange: { page: string; id?: number } }>();

	let id_barang = '';
	let nama_barang = '';
	let deskripsi = '';
	let jumlah = 0;
	let kategori = '';
	let img: File | null = null;
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

	// Penanganan file input dengan tipe aman untuk TS
	const handleFileChange = (event: Event) => {
		const inputHTML = event.target as HTMLInputElement;
		if (inputHTML.files && inputHTML.files.length > 0) {
			img = inputHTML.files[0];
		}
	};
</script>

<form onsubmit={tambah_barang} class="space-y-4">
	<div>
		<label for="id_barang">ID Barang</label>
		<input id="id_barang" type="text" bind:value={id_barang} required />
	</div>

	<div>
		<label for="nama_barang">Nama Barang</label>
		<input id="nama_barang" type="text" bind:value={nama_barang} required />
	</div>

	<div>
		<label for="jumlah">Jumlah</label>
		<input id="jumlah" type="number" bind:value={jumlah} min="0" required />
	</div>

	<div>
		<label for="kategori">Kategori</label>
		<input id="kategori" type="text" bind:value={kategori} required />
	</div>

	<div>
		<label for="deskripsi">Deskripsi</label>
		<input id="deskripsi" type="text" bind:value={deskripsi} required />
	</div>

	<div>
		<label for="img">Gambar</label>
		<input id="img" type="file" onchange={handleFileChange} />
	</div>

	{#if successMessage}<p class="text-green-600">{successMessage}</p>{/if}
	{#if errorMessage}<p class="text-red-600">{errorMessage}</p>{/if}

	<button type="submit" disabled={isLoading}>
		{#if isLoading}Menyimpan...{:else}Tambah Barang{/if}
	</button>

	<button type="button" onclick={() => dispatch('pageChange', { page: 'Barang' })}>
		Kembali
	</button>
</form>
