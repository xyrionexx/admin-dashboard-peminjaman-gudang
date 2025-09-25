<script lang="ts">
	// Correct paths with index.js extension to avoid TypeScript errors
	import * as Table from '$lib/components/ui/table/index.js';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import * as Pagination from '$lib/components/ui/pagination/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import Icon from '@iconify/svelte';
	import { createEventDispatcher, onMount } from 'svelte';
	import { passive } from 'svelte/legacy';

	// Define a type with index signature to allow dynamic access to properties
	interface UserData {
		[key: string]: any;
	}

	type CategoryType = 'Siswa' | 'Guru' | 'Pegawai' | '';

	const dispatch = createEventDispatcher<{
		pageChange: { page: string; id?: number; kategori?: string };
	}>();
	function updateUser() {}

	let siswa: any[] = $state([]);
	let guru: any[] = $state([]);
	let pegawai: any[] = $state([]);
	let search = $state('');
	let value = $state('Siswa'); // Default to Siswa view
	let loading = $state(true);
	let currentPage = $state(1);
	const perPage = 10;

	onMount(async () => {
		try {
			const [resSiswa, resGuru, resPegawai] = await Promise.all([
				fetch('http://127.0.0.1:8000/api/siswa/'),
				fetch('http://127.0.0.1:8000/api/guru/'),
				fetch('http://127.0.0.1:8000/api/pegawai')
			]);

			siswa = await resSiswa.json();
			guru = await resGuru.json();
			pegawai = await resPegawai.json();
		} catch (err) {
			console.error(err);
		} finally {
			loading = false;
		}
	});

	const categories = $derived([
		...(siswa.length ? ['Siswa'] : []),
		...(guru.length ? ['Guru'] : []),
		...(pegawai.length ? ['Pegawai'] : [])
	]);

	const triggerContent = $derived(
		value ? (categories.find((c) => c === value) ?? 'Select a User') : 'Select a User'
	);

	const allData = $derived([
		...siswa.map((s) => ({
			id: s.nis,
			nama: s.nama_siswa,
			keterangan: s.kelas,
			kartu: s.kartu_pelajar,
			no_telp: s.no_telp,
			email: s.email,
			password: s.password,
			kategori: 'Siswa',
			raw_data: s
		})),
		...guru.map((g) => ({
			id: g.nuptk,
			nama: g.nama_guru,
			keterangan: g.bidang,
			kartu: '-',
			no_telp: g.no_telp,
			email: g.email,
			password: g.password,
			kategori: 'Guru',
			raw_data: g
		})),
		...pegawai.map((p) => ({
			id: p.id_pegawai,
			nama: p.nama_pegawai,
			keterangan: p.bidang,
			kartu: '-',
			no_telp: p.no_telp,
			email: p.email,
			password: p.password,
			kategori: 'Pegawai',
			raw_data: p
		}))
	]);

	const filteredData = $derived(
		allData.filter((item) => {
			const matchCategory = !value || item.kategori === value;
			const matchSearch =
				!search ||
				item.nama?.toLowerCase().includes(search.toLowerCase()) ||
				item.keterangan?.toLowerCase().includes(search.toLowerCase());
			return matchCategory && matchSearch;
		})
	);

	const totalData = $derived(() => filteredData.length);

	const paginatedData = $derived(() => {
		const start = (currentPage - 1) * perPage;
		const end = start + perPage;
		return filteredData.slice(start, end);
	});

	async function deleteUser(id: string, kategori: string) {
		if (!confirm('Apakah anda yakin ingin menghapus data ini ?')) return;
		console.log(id, kategori);

		try {
			let res;
			if (kategori === 'Siswa') {
				res = await fetch(`http://127.0.0.1:8000/api/siswa/delete/${id}/`, {
					method: 'DELETE'
				});
			} else if (kategori === 'Guru') {
				res = await fetch(`http://127.0.0.1:8000/api/guru/delete/${id}/`, {
					method: 'DELETE'
				});
			} else if (kategori === 'Pegawai') {
				res = await fetch(`http://127.0.0.1:8000/api/pegawai/delete/${id}/`, {
					method: 'DELETE'
				});
			}

			if (!res?.ok) {
				throw new Error('Gagal menghapus data');
			}

			if (kategori === 'Siswa') {
				siswa = siswa.filter((s) => s.nis !== id);
			} else if (kategori === 'Guru') {
				guru = guru.filter((g) => g.nuptk !== id);
			} else if (kategori === 'Pegawai') {
				pegawai = pegawai.filter((p) => p.id_pegawai !== id);
			}

			alert('Data berhasil dihapus');
		} catch (err) {
			console.error(err);
			alert('Terjadi kesalahan saat menghapus data');
		}
	}

	// Function to get specific columns based on selected user type
	function getColumnHeaders(type: string) {
		switch (type) {
			case 'Siswa':
				return [
					{ key: 'id', label: 'NIS' },
					{ key: 'nama', label: 'Nama Siswa' },
					{ key: 'keterangan', label: 'Kelas' },
					{ key: 'kartu', label: 'Kartu Pelajar' },
					{ key: 'no_telp', label: 'No Telepon' },
					{ key: 'email', label: 'Email' },
					{ key: 'action', label: 'Aksi' }
				];
			case 'Guru':
				return [
					{ key: 'id', label: 'NUPTK' },
					{ key: 'nama', label: 'Nama Guru' },
					{ key: 'keterangan', label: 'Bidang' },
					{ key: 'no_telp', label: 'No Telepon' },
					{ key: 'email', label: 'Email' },
					{ key: 'action', label: 'Aksi' }
				];
			case 'Pegawai':
				return [
					{ key: 'id', label: 'ID Pegawai' },
					{ key: 'nama', label: 'Nama Pegawai' },
					{ key: 'keterangan', label: 'Bidang' },
					{ key: 'no_telp', label: 'No Telepon' },
					{ key: 'email', label: 'Email' },
					{ key: 'action', label: 'Aksi' }
				];
			default:
				return [];
		}
	}

	const columnHeaders = $derived(getColumnHeaders(value));

	interface PageInfo {
		key: string;
		value: number;
		type?: string;
	}

	// Helper function to access user data safely
	function getUserData(user: UserData, key: string): any {
		return user[key];
	}
</script>

<h1 class="mb-6 text-4xl font-bold text-blue-600">DATA USERS</h1>

<!-- Controls section -->
<div class="mb-6 rounded-lg bg-white p-6 shadow-sm">
	<div class="flex flex-col items-center justify-between gap-4 md:flex-row">
		<!-- User Type Selector -->
		<div class="w-64">
			<label for="user-type" class="mb-1 block text-sm font-medium text-gray-700"
				>Pilih Tipe Pengguna</label
			>
			<!-- Using manual selection with regular select to avoid TypeScript errors -->
			<select
				class="w-full rounded-md border border-blue-200 bg-white p-2"
				onchange={(e) => (value = (e.target as HTMLSelectElement).value as CategoryType)}
			>
				{#each categories as category}
					<option value={category} selected={category === value}>{category}</option>
				{/each}
			</select>
		</div>

		<!-- Search -->
		<div class="relative w-64">
			<label for="search" class="mb-1 block text-sm font-medium text-gray-700">Cari</label>
			<div class="relative">
				<input
					id="search"
					class="w-full rounded-md border border-blue-200 py-2 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
					type="text"
					placeholder="Cari nama atau keterangan..."
					bind:value={search}
				/>
				<div class="absolute left-3 top-2.5 text-blue-400">
					<Icon icon="heroicons:magnifying-glass" width="20" height="20" />
				</div>
			</div>
		</div>

		<!-- Add User Button -->
		<button
			class="mt-6 rounded-lg bg-blue-500 p-2 px-4 text-white transition-colors hover:bg-blue-600"
			onclick={() => dispatch('pageChange', { page: 'TambahUser' })}
		>
			<div class="flex items-center gap-2">
				<Icon icon="heroicons:plus" />
				Tambah User
			</div>
		</button>
	</div>
</div>

<!-- Stats Card -->
<div class="mb-6 flex gap-6">
	<div class="flex-1 overflow-hidden rounded-lg bg-white shadow-sm">
		<div class="flex items-center p-5">
			<div class="mr-4 rounded-full bg-blue-100 p-3">
				<Icon icon="heroicons:users" class="text-blue-600" width="24" height="24" />
			</div>
			<div>
				<h2 class="text-lg font-medium text-gray-600">Jumlah {value}</h2>
				<h2 class="text-2xl font-bold text-blue-800">{totalData()}</h2>
			</div>
		</div>
	</div>
</div>

<!-- Table Container -->
<div class="overflow-hidden rounded-lg bg-white p-6 shadow-sm">
	{#if loading}
		<div class="flex items-center justify-center py-16">
			<div class="h-12 w-12 animate-spin rounded-full border-b-2 border-t-2 border-blue-500"></div>
		</div>
	{:else}
		<!-- Dynamic Table Headers Based on Selected User Type -->
		<div class="overflow-x-auto">
			<Table.Root>
				<Table.Header>
					<Table.Row class="bg-blue-50">
						{#each columnHeaders as header}
							<Table.Head class="font-semibold text-blue-800">{header.label}</Table.Head>
						{/each}
					</Table.Row>
				</Table.Header>
				<Table.Body>
					{#if paginatedData().length === 0}
						<Table.Row>
							<Table.Cell colspan={columnHeaders.length} class="py-10 text-center text-gray-500">
								Tidak ada data {value} yang ditemukan
							</Table.Cell>
						</Table.Row>
					{:else}
						{#each paginatedData() as user, i}
							<Table.Row class={i % 2 === 0 ? 'bg-white' : 'bg-blue-50/30'}>
								{#each columnHeaders as header}
									{#if header.key === 'kartu' && user.kategori === 'Siswa'}
										<Table.Cell>
											{#if user.kartu && user.kartu !== '-'}
												<img
													src={user.kartu}
													alt="Kartu Pelajar"
													class="h-10 w-16 object-contain"
												/>
											{:else}
												<span class="text-gray-400">-</span>
											{/if}
										</Table.Cell>
									{:else if header.key === 'action'}
										<Table.Cell>
											<div class="flex gap-2">
												<button
													class="rounded bg-blue-100 p-1.5 text-blue-600 hover:bg-blue-200"
													onclick={() =>
														dispatch('pageChange', {
															page: 'UpdateUser',
															id: user.id,
															kategori: user.kategori
														})}
												>
													<Icon icon="heroicons:pencil-square" width="18" height="18" />
												</button>
												<button
													class="rounded bg-red-100 p-1.5 text-red-600 hover:bg-red-200"
													onclick={() => deleteUser(String(user.id), user.kategori)}
												>
													<Icon icon="heroicons:trash" width="18" height="18" />
												</button>
											</div>
										</Table.Cell>
									{:else}
										<Table.Cell>
											<span>{getUserData(user, header.key) || '-'}</span>
										</Table.Cell>
									{/if}
								{/each}
							</Table.Row>
						{/each}
					{/if}
				</Table.Body>
			</Table.Root>
		</div>

		<!-- Pagination -->
		{#if totalData() > perPage}
			<div class="mt-6 flex justify-center">
				<Pagination.Root
					count={Math.ceil(totalData() / perPage)}
					{perPage}
					page={currentPage}
					onPageChange={(p) => (currentPage = p)}
				>
					{#snippet children({ pages, currentPage }: { pages: any[]; currentPage: number })}
						<Pagination.Content>
							<Pagination.Item>
								<Pagination.PrevButton />
							</Pagination.Item>
							{#each pages as page (page.key)}
								{#if page.type === 'ellipsis'}
									<Pagination.Item>
										<Pagination.Ellipsis />
									</Pagination.Item>
								{:else}
									<Pagination.Item>
										<Pagination.Link {page} isActive={currentPage === page.value}>
											{page.value}
										</Pagination.Link>
									</Pagination.Item>
								{/if}
							{/each}
							<Pagination.Item>
								<Pagination.NextButton />
							</Pagination.Item>
						</Pagination.Content>
					{/snippet}
				</Pagination.Root>
			</div>
		{/if}
	{/if}
</div>
