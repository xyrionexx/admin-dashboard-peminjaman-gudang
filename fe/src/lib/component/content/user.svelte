<script lang="ts">
	import * as Table from '$lib/components/ui/table/index.js';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import * as Pagination from '$lib/components/ui/pagination/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import Icon from '@iconify/svelte';
	import { createEventDispatcher, onMount } from 'svelte';

	const dispatch = createEventDispatcher<{ pageChange: { page: string; id?: number } }>();
	function updateUser() {}

	let siswa: any[] = $state([]);
	let guru: any[] = $state([]);
	let search = $state('');
	let value = $state('');
	let loading = true;
	let currentPage = $state(1);
	const perPage = 10;

	onMount(async () => {
		try {
			const [resSiswa, resGuru] = await Promise.all([
				fetch('http://127.0.0.1:8000/api/siswa/'),
				fetch('http://127.0.0.1:8000/api/guru/')
			]);

			siswa = await resSiswa.json();
			guru = await resGuru.json();
		} catch (err) {
			console.error(err);
		} finally {
			loading = false;
		}
	});

	const categories = $derived([
		...(siswa.length ? ['Siswa'] : []),
		...(guru.length ? ['Guru'] : [])
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
			kategori: 'Siswa'
		})),
		...guru.map((g) => ({
			id: g.nuptk,
			nama: g.nama_guru,
			keterangan: g.bidang,
			kartu: '-',
			no_telp: g.no_telp,
			kategori: 'Guru'
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

	async function deleteUser(id: number, kategori: string) {
		if (!confirm('Apakah anda yakin ingin menghapus data ini ?')) return;

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
			}

			if (!res?.ok) {
				throw new Error('Gagal menghapus data');
			}

			if (kategori === 'Siswa') {
				siswa = siswa.filter((s) => s.nis !== id);
			} else {
				guru = guru.filter((g) => g.nuptk !== id);
			}

			alert('Data berhasil dihapus');
		} catch (err) {
			console.error(err);
			alert('Terjadi kesalahan saat menghapus data');
		}
	}
</script>

<h1 class="text-4xl font-bold">DATA USERS</h1>

<div class="flex w-full justify-end">
	<button
		class="mb-10 rounded-2xl bg-blue-400 p-2 px-3 text-white hover:bg-blue-600"
		onclick={() => dispatch('pageChange', { page: 'TambahUser' })}
	>
		Tambah data
	</button>
</div>

<div class="mb-10 flex gap-10">
	<div class="flex w-[30vw] flex-col gap-3 rounded-2xl border-2 border-gray-300 bg-white p-5">
		<h2 class="text-2xl font-medium">Jumlah User</h2>
		<h2 class="text-2xl">{totalData()}</h2>
	</div>
	<div class="flex w-[30vw] flex-col gap-3 rounded-2xl border-2 border-gray-300 bg-white p-5">
		<h2 class="text-2xl font-medium">Total Barang</h2>
		<h2 class="text-2xl">20</h2>
	</div>
</div>

<div class="rounded-4xl flex flex-col bg-gray-100">
	<div class="menubar flex h-[10vh] items-center gap-5 pl-4">
		<div>
			<Select.Root type="single" name="userCategory" bind:value>
				<Select.Trigger class="w-[180px] bg-white py-5">
					{triggerContent}
				</Select.Trigger>
				<Select.Content>
					<Select.Group>
						<Select.Label>Category</Select.Label>
						<Select.Item value="">All</Select.Item>
						{#each categories as kategori}
							<Select.Item value={kategori}>{kategori}</Select.Item>
						{/each}
					</Select.Group>
				</Select.Content>
			</Select.Root>
		</div>
		<div class="search relative mb-2 mt-2 flex w-[20vw] rounded-sm border-[1px] bg-white p-0 px-1">
			<Icon
				icon="line-md:search"
				class="absolute left-2 top-2"
				width="24"
				height="24"
				style="color: #000"
			/>
			<input
				type="text"
				placeholder="Search..."
				class="w-full py-2 pl-9 outline-none"
				bind:value={search}
			/>
		</div>
	</div>

	<div class="rounded-4xl bg-white p-2 px-4">
		<Table.Root class="mb-5">
			<Table.Header>
				<Table.Row class="border-b-2 border-black">
					<Table.Head class="w-[100px] border-r-[1px] border-black">ID</Table.Head>
					<Table.Head>Nama</Table.Head>
					<Table.Head>Keterangan</Table.Head>
					<Table.Head class="text-right">Kartu</Table.Head>
					<Table.Head class="text-right">NO Telp</Table.Head>
					<Table.Head class="text-right">Kategori</Table.Head>
					<Table.Head class="text-right">Button</Table.Head>
				</Table.Row>
			</Table.Header>
			<Table.Body>
				{#each paginatedData() as user}
					<Table.Row class="border-b-[1px] border-black">
						<Table.Cell class="border-r-[1px] border-black font-medium text-black">
							{user.id}
						</Table.Cell>
						<Table.Cell>{user.nama}</Table.Cell>
						<Table.Cell>{user.keterangan}</Table.Cell>
						<Table.Cell class="text-right">
							<img
								src={user.kartu}
								alt="Kartu Pelajar"
								class="h-16 w-16 object-contain"
							/></Table.Cell
						>
						<Table.Cell class="text-right">{user.no_telp}</Table.Cell>
						<Table.Cell class="text-right">{user.kategori}</Table.Cell>
						<Table.Cell class="flex justify-end">
							<DropdownMenu.Root>
								<DropdownMenu.Trigger>
									<Icon icon="mi:options-vertical" width="20" height="20" />
								</DropdownMenu.Trigger>
								<DropdownMenu.Content>
									<DropdownMenu.Group>
										<DropdownMenu.Label>Action</DropdownMenu.Label>
										<DropdownMenu.Separator />
										<DropdownMenu.Item>
											<button onclick={() => deleteUser(user.id, user.kategori)}>Delete</button>
										</DropdownMenu.Item>
										<DropdownMenu.Item>
											<a
												class="w-[100%]"
												href={`/update/${user.kategori.toLowerCase()}/${user.id}`}
											>
												Update
											</a>
										</DropdownMenu.Item>
									</DropdownMenu.Group>
								</DropdownMenu.Content>
							</DropdownMenu.Root>
						</Table.Cell>
					</Table.Row>
				{/each}
			</Table.Body>
		</Table.Root>

		<Pagination.Root count={totalData()} {perPage} bind:page={currentPage}>
			{#snippet children({ pages, currentPage })}
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
</div>
