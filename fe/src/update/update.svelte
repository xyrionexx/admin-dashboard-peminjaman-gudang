<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';

	export let id: number;
	const dispatch = createEventDispatcher<{ pageChange: { page: string; id?: number } }>();

	let nama = '';
	let jumlah: number = 0;
	let kategori = '';
	let deskripsi = '';

	onMount(async () => {
		if (!id) return;
		try {
			const res = await fetch(`http://127.0.0.1:8000/api/barang/${id}/`);
			if (!res.ok) throw new Error('Data tidak ditemukan');
			const data = await res.json();
			nama = data.nama_barang;
			jumlah = data.jumlah;
			kategori = data.kategori;
			deskripsi = data.deskripsi;
		} catch (err) {
			console.error(err);
			alert('Gagal mengambil data barang');
		}
	});

	async function saveUpdate() {
		try {
			const res = await fetch(`http://127.0.0.1:8000/api/barang/${id}/`, {
				method: 'PUT',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ nama_barang: nama, jumlah, kategori, deskripsi })
			});
			if (!res.ok) throw new Error('Gagal update data');
			alert('Data berhasil diperbarui');
			dispatch('pageChange', { page: 'Barang' });
		} catch (err) {
			console.error(err);
			alert('Terjadi kesalahan saat update');
		}
	}

	function cancel() {
		dispatch('pageChange', { page: 'Barang' });
	}
</script>

<div class="mx-auto my-8 max-w-md rounded-xl border border-blue-50 bg-white p-8 shadow-lg">
	<h1 class="mb-8 text-center text-3xl font-semibold tracking-tight text-blue-800">
		Update Barang
	</h1>

	<form on:submit|preventDefault={saveUpdate} class="space-y-6">
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

		<div class="space-y-2">
			<label for="deskripsi" class="block text-sm font-medium text-gray-700">Deskripsi</label>
			<input
				id="deskripsi"
				type="text"
				bind:value={deskripsi}
				required
				class="focus:ring-3 w-full rounded-lg border-2 border-blue-100 bg-blue-50/30 px-3 py-3 text-base transition-all duration-200 hover:border-blue-200 hover:bg-white focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-blue-100"
			/>
		</div>

		<div class="flex flex-col justify-center gap-4 pt-4 sm:flex-row">
			<button
				type="submit"
				class="focus:ring-3 min-w-[120px] rounded-lg bg-gradient-to-r from-blue-500 to-blue-700 px-8 py-3 font-medium text-white transition-all duration-200 hover:-translate-y-0.5 hover:from-blue-600 hover:to-blue-800 hover:shadow-lg focus:outline-none focus:ring-blue-300 active:translate-y-0"
			>
				Update
			</button>
			<button
				type="button"
				class="focus:ring-3 min-w-[120px] rounded-lg border border-slate-200 bg-slate-100 px-8 py-3 font-medium text-slate-600 transition-all duration-200 hover:-translate-y-0.5 hover:bg-slate-200 hover:text-slate-700 hover:shadow-md focus:outline-none focus:ring-slate-200 active:translate-y-0"
				on:click={cancel}
			>
				Cancel
			</button>
		</div>
	</form>
</div>
